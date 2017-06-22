from django import forms
from django.core.validators import FileExtensionValidator


class ExportForm(forms.Form):
    h_input = forms.HiddenInput()


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Upload csv', validators=[FileExtensionValidator(allowed_extensions=['csv'])])

