from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests
import base64
from rest_framework import generics
from .models import Image, PurchasePrediction
from .forms import ImageForm, ImageUploadForm, PredictionForm
from .serializers import ImageSerializer
from .ml_service import ml_service

def gallery_list(request):
    images = Image.objects.all()
    return render(request, 'gallery/gallery_list.html', {'images': images})

def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image ajoutée avec succès !')
            return redirect('gallery_list')
    else:
        form = ImageForm()
    
    return render(request, 'gallery/add_image.html', {'form': form})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            
            try:
                image_file = request.FILES['image_file']
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                api_key = 'c00a1a05dd57a9ea7951a0a0bb0cad72'
                url = 'https://api.imgbb.com/1/upload'
                
                payload = {
                    'key': api_key,
                    'image': image_base64,
                    'name': image_instance.title
                }
                
                response = requests.post(url, data=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    if result['success']:
                        image_url = result['data']['url']
                        image_instance.url = image_url
                        image_instance.image_file = None
                        image_instance.save()
                        messages.success(request, f'Image uploadée avec succès sur ImgBB !')
                        return redirect('gallery_list')
                    else:
                        messages.error(request, f'Erreur ImgBB: {result.get("error", "Erreur inconnue")}')
                else:
                    messages.error(request, f'Erreur HTTP {response.status_code}: {response.text}')
                    
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'upload: {str(e)}')
                image_instance.save()
                messages.warning(request, 'Image sauvegardée localement (upload ImgBB échoué)')
                return redirect('gallery_list')
    else:
        form = ImageUploadForm()
    
    return render(request, 'gallery/upload_image.html', {'form': form})

class ImageListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    def get_queryset(self):
        queryset = Image.objects.all()
        source = self.request.query_params.get('source', None)
        
        if source == 'imgbb':
            queryset = queryset.filter(url__isnull=False)
        elif source == 'local':
            queryset = queryset.filter(image_file__isnull=False, url__isnull=True)
        
        return queryset.order_by('-created_at')

def prediction_form(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            estimated_salary = form.cleaned_data['estimated_salary']
            
            prediction_result = ml_service.predict_purchase(age, gender, estimated_salary)
            
            if prediction_result['success']:
                prediction = PurchasePrediction.objects.create(
                    age=age,
                    gender=gender,
                    estimated_salary=estimated_salary,
                    will_purchase=prediction_result['will_purchase'],
                    confidence=prediction_result['confidence'] * 100,
                    probability_purchase=prediction_result['probability_purchase'] * 100,
                    probability_no_purchase=prediction_result['probability_no_purchase'] * 100,
                    model_name=prediction_result['model_name'],
                    model_accuracy=prediction_result['accuracy']
                )
                
                messages.success(request, 'Prédiction effectuée avec succès !')
                return render(request, 'gallery/prediction_result.html', {
                    'prediction': prediction,
                    'form': PredictionForm()
                })
            else:
                messages.error(request, f"Erreur lors de la prédiction: {prediction_result['error']}")
    else:
        form = PredictionForm()
    
    recent_predictions = PurchasePrediction.objects.all()[:10]
    
    return render(request, 'gallery/prediction_form.html', {
        'form': form,
        'recent_predictions': recent_predictions,
        'model_info': ml_service.get_model_info()
    })

def prediction_history(request):
    predictions = PurchasePrediction.objects.all()
    return render(request, 'gallery/prediction_history.html', {
        'predictions': predictions
    })