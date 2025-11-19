import csv
import io
from celery import shared_task
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Upload, Person

@shared_task(bind=True)
def proc_csv(self, upload_id):
    try:
        upload = Upload.objects.get(id=upload_id)
        if upload:
            upload.status = 'processing'
            upload.save()
    except Upload.DoesNotExist:
        return {'status': 'error', 'message': f'Upload {upload_id} not found'}

    error = []
    processed = 0
    total = 0

    with upload.file.open('rb') as files:
        data = files.read()
