from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Your message has been sent to the app admin. Thanks for getting in touch.",
        )
        return redirect("contact:contact")
    return render(request, "contact/contact.html", {"form": form})
