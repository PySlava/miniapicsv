import csv
import io
import json
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Upload, Person


@shared_task(bind=True)
def process_csv(self, upload_id):
    try:
        upload = Upload.objects.get(id=upload_id)
    except Upload.DoesNotExist:
        return {"status": "error", "message": f"Upload {upload_id} not found"}

    upload.status = Upload.STATUS_PROCESSING
    upload.save()

    errors = []
    processed = 0

    with upload.file.open("rb") as f:
        raw_data = f.read()

    try:
        text = raw_data.decode("utf-8")
    except UnicodeDecodeError:
        upload.status = Upload.STATUS_ERROR
        upload.error = "File encoding is not UTF-8"
        upload.save()
        return {"status": "failed", "reason": "encoding"}

    reader = csv.DictReader(io.StringIO(text))
    required = {"name", "email", "age"}

    if not required.issubset(reader.fieldnames or []):
        upload.status = Upload.STATUS_ERROR
        upload.error = f"CSV must contain columns: {required}"
        upload.save()
        return {"status": "failed", "reason": "columns"}

    rows = list(reader)
    upload.total_rows = len(rows)
    upload.save()

    for i, row in enumerate(rows, start=1):
        name = row.get("name", "").strip()
        email = row.get("email", "").strip()
        age_raw = row.get("age", "").strip()

        row_errors = []

        if not name:
            row_errors.append("name empty")

        try:
            validate_email(email)
        except ValidationError:
            row_errors.append("invalid email")

        try:
            age = int(age_raw)
            if age < 0 or age > 100:
                row_errors.append("age out of range")
        except Exception:
            row_errors.append("invalid age")
        if row_errors:
            errors.append({"row": i, "errors": row_errors, "raw": row})
            continue

        Person.objects.create(
            upload=upload,
            name=name,
            email=email,
            age=age
        )
        processed += 1

        if processed % 50 == 0:
            upload.processed_rows = processed
            upload.save()

    upload.processed_rows = processed
    upload.status = Upload.STATUS_DONE if not errors else Upload.STATUS_ERROR
    upload.error = json.dumps(errors[:50], ensure_ascii=False)
    upload.save()

    return {
        "status": upload.status,
        "processed": processed,
        "errors": len(errors),
    }
