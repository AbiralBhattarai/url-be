from django.db import models

# Create your models here.


class ShortURL(models.Model):
    original_url = models.TextField()
    shortened_url = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.original_url}--->{self.shortened_url}"


class Click(models.Model):
    url = models.ForeignKey(ShortURL,on_delete=models.CASCADE,related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Click on {self.url.shortened_url}"