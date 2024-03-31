import uuid

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from manager.forms import CustomManagerCreationForm, CustomAuthenticationForm


@ensure_csrf_cookie
@csrf_exempt
def registration_manager(request):
    if request.method == 'POST':
        form = CustomManagerCreationForm((request.POST), exclude_company_identifier=True)
        print(form)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.status = 2  # Устанавливаем статус "Компания"
            manager.company_identifier = str(uuid.uuid4())
            manager.save()
            login(request, manager)
            print("Manager saved successfully.")
            return redirect('')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = CustomManagerCreationForm(exclude_company_identifier=True)
    return render(request, 'manager/registration_manager.html', {'form': form})


def authentication(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            return redirect('registration_manager')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'manager/authentication.html', {'form': form})
