from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    image_file = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    @property
    def image_url(self):
        if self.url:
            return self.url
        elif self.image_file:
            return self.image_file.url
        return None
    
    class Meta:
        ordering = ['-created_at']

class PurchasePrediction(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    estimated_salary = models.IntegerField()
    
    will_purchase = models.BooleanField()
    confidence = models.FloatField()
    probability_purchase = models.FloatField()
    probability_no_purchase = models.FloatField()
    
    model_name = models.CharField(max_length=100)
    model_accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prédiction {self.id}: {self.gender}, {self.age}ans, {self.estimated_salary}€ -> {'Achat' if self.will_purchase else 'Pas d\'achat'}"
    
    class Meta:
        ordering = ['-created_at']