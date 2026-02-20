from django import forms
from .models import PropertyReport


class PropertyReportForm(forms.ModelForm):
    class Meta:
        model = PropertyReport
        fields = [
            "house_number",
            "violation",
            "description",
            "image",  # 🔥 must match the model field name
            "latitude",
            "longitude",
        ]
        widgets = {
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
