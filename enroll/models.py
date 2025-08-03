from django.db import models

# Create your models here.
class newuser(models.Model):
    Username=models.CharField(max_length=80)
    fname=models.CharField(max_length=89)
    lname=models.CharField(max_length=88)
    email=models.EmailField(max_length=90)
    pass1=models.CharField(max_length=90)
    pass2=models.CharField(max_length=90)



class PredictedImage(models.Model):
    image = models.ImageField(upload_to='predicted_images/')
    # Add other fields if needed




class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, null='True')
    phone = models.CharField(max_length=10, null='True')
    desc = models.TextField(null='True')


from django.db import models

class PredictedVideo(models.Model):
    uploaded_video = models.FileField(upload_to="uploaded_videos/", null=True)
    processed_video = models.FileField(upload_to="processed_videos/",null=True)
    detected_label = models.CharField(max_length=255, default="Not Detected")
    created_at = models.DateTimeField(auto_now_add=True)



from django.db import models

class VideoUpload(models.Model):
    original_video = models.FileField(upload_to='videos/original/')
    processed_video = models.FileField(upload_to='videos/processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)



# from django.db import models

# class CheatingDetection(models.Model):
#     timestamp = models.CharField(max_length=100)
#     detected_class = models.CharField(max_length=100)
#     confidence = models.FloatField()
#     frame_number = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.detected_class} at {self.timestamp}"



from django.db import models

class CheatingDetection(models.Model):
    timestamp = models.CharField(max_length=20)
    detected_class = models.CharField(max_length=50)
    confidence = models.FloatField()
    frame_number = models.IntegerField()
    screenshot = models.ImageField(upload_to='detections/', null='True')

    def __str__(self):
        return f"{self.detected_class} at {self.timestamp}"
