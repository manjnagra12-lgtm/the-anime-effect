from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"maxlength": 150}),
            "message": forms.Textarea(
                attrs={
                    "rows": 6,
                    "maxlength": 3000,
                    "placeholder": "Tell us what you have in mind...",
                }
            ),
        }
