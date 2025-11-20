from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import UploadForm
from .models import Upload, Person
from .serializers import UploadSerializer, PersonSerializer
from .tasks import process_csv


class UploadView(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {"detail": "CSV file is required under 'file' field"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not file.name.lower().endswith('.csv'):
            return Response(
                {"detail": "Only files with .csv are allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        upload = Upload.objects.create(file=file, status=Upload.STATUS_PENDING)
        process_csv.delay(upload.id)
        serializer = UploadSerializer(upload)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UploadPageView(FormView):
    template_name = 'recordcsv/upload_csv.html'
    form_class = UploadForm
    success_url = reverse_lazy('upload_page')

    def form_valid(self, form):
        file = form.cleaned_data['file']

        upload = Upload.objects.create(file=file, status=Upload.STATUS_PENDING)
        process_csv.delay(upload.id)
        messages.success(self.request, "File uploaded successfully! Processing started.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please upload a valid CSV file.")
        return super().form_invalid(form)


class UserListView(APIView):
    def get(self, request):
        users = Person.objects.all().order_by('-created_at')
        serializer = PersonSerializer(users, many=True)
        return Response(serializer.data)
