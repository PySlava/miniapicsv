from django import forms


class UploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.lower().endswith('.csv'):
            raise forms.ValidationError('Only CSV files is correct')

        return file
