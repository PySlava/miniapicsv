from django.db import models

class Upload(models.Model):
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending')
    total_rows = models.IntegerField(null=True, blank=True)
    process = models.IntegerField(default=0)
    error = models.TextField(blank=True)

    def __str__(self):
        return f'Upload {self.pk} - {self.status}'


class Person(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='persons')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'

