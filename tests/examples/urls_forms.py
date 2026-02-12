from django.urls import path
try:
    from django.shortcuts import render
    from .choice_form_howto import (
        TextChoicesExampleForm as TextChoicesExampleForm,
        TextChoicesExample as TextChoicesExample
    )
    from .flag_form_howto import (
        PermissionsExampleForm as PermissionsExampleForm,
        Group as Group
    )

    def choice_form_view(request):
        from .choice_form_howto import TextChoicesExampleForm, form
        if request.method == "POST":
            form = TextChoicesExampleForm(request.POST)
            if form.is_valid():
                # Process the form data (for now, just print it)
                print("Valid form data:", form.cleaned_data)
        return render(request, "tests_examples/choice_form_howto.html", {"form": form})
    
    def radio_form_view(request):
        from .radio_form_howto import TextChoicesExampleForm, form
        if request.method == "POST":
            form = TextChoicesExampleForm(request.POST)
            if form.is_valid():
                # Process the form data (for now, just print it)
                print("Valid form data:", form.cleaned_data)
        return render(request, "tests_examples/choice_form_howto.html", {"form": form})

    def flag_form_view(request):
        from .flag_form_howto import PermissionsExampleForm, form
        if request.method == "POST":
            form = PermissionsExampleForm(request.POST)
            if form.is_valid():
                # Process the form data (for now, just print it)
                print("Valid form data:", form.cleaned_data)
        return render(request, "tests_examples/flag_form_howto.html", {"form": form})

    def checkboxes_form_view(request):
        from .checkboxes_form_howto import PermissionsExampleForm, form
        if request.method == "POST":
            form = PermissionsExampleForm(request.POST)
            if form.is_valid():
                # Process the form data (for now, just print it)
                print("Valid form data:", form.cleaned_data)
        return render(request, "tests_examples/flag_form_howto.html", {"form": form})

    app_name = "howto_forms"

    urlpatterns = [
        path("choice/", choice_form_view, name="choice"),
        path("radio/", radio_form_view, name="radio"),
        path("flag/", flag_form_view, name="flag"),
        path("checkboxes/", checkboxes_form_view, name="checkboxes"),
    ]
except ImportError:
    urlpatterns = []
