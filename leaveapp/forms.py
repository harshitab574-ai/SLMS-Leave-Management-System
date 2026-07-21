from django import forms
from .models import Staff, Leave

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        exclude = ["status"]

        widgets = {
            "staff": forms.Select(attrs={"class": "form-select"}),
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "from_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "to_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }