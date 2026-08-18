from django import forms
from .models import Staff, Leave
from django.utils import timezone


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'name',
            'email',
            'phone',
            'department',
            'designation',
            'address',
            'joining_date',
            'image'
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class LeaveForm(forms.ModelForm):

    class Meta:
        model = Leave

        fields = [
            'leave_type',
            'reason',
            'from_date',
            'to_date'
        ]

        widgets = {
            'reason': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter leave reason'
                }
            ),

            'from_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'to_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date:

            if from_date < timezone.now().date():
                raise forms.ValidationError(
                    "From date cannot be in the past."
                )

            if to_date < from_date:
                raise forms.ValidationError(
                    "To date cannot be before From date."
                )

        return cleaned_data