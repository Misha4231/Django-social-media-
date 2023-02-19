from django import forms
from .models import Image

class FileCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'file', 'description')