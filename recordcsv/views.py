from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Upload
from .serializers import UploadSerializer
from .tasks import proc_csv

class UploadView(APIView):
    def post(self, request, format):
        file = request.FILES.get('file')
        if not file:
            return Response({"detail": "CSV file is required under 'file' field"}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.lower().endswith('.csv'):
            return Response({"detail": "Only files with .csv are correct"}, status=status.HTTP_400_BAD_REQUEST)

        upload = Upload.objects.create(file=file, status='pending')
        proc_csv.delay(upload.id)
        serializer = UploadSerializer(upload)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
