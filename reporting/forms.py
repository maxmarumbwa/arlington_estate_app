from django import forms
from .models import PropertyReport


class PropertyReportForm(forms.ModelForm):
    class Meta:
        model = PropertyReport
        fields = [
            "house_number",
            "violation",
            "description",
            "latitude",
            "longitude",
            "image",  # include single image
        ]
        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
