from django.contrib import admin
from .models import Image, PurchasePrediction

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'created_at']
    search_fields = ['title']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

@admin.register(PurchasePrediction)
class PurchasePredictionAdmin(admin.ModelAdmin):
    list_display = ['gender', 'age', 'estimated_salary', 'will_purchase', 'confidence', 'created_at']
    list_filter = ['will_purchase', 'gender', 'model_name', 'created_at']
    search_fields = ['gender']
    readonly_fields = ['created_at', 'model_name', 'model_accuracy']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Profil utilisateur', {
            'fields': ('age', 'gender', 'estimated_salary')
        }),
        ('Prédiction', {
            'fields': ('will_purchase', 'confidence', 'probability_purchase', 'probability_no_purchase')
        }),
        ('Métadonnées', {
            'fields': ('model_name', 'model_accuracy', 'created_at'),
            'classes': ('collapse',)
        }),
    )