import json
import uuid

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from manager.forms import CustomManagerCreationForm, CustomAuthenticationForm, CustomDeveloperCreationForm
from manager.models import User

@ensure_csrf_cookie
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode('utf-8'))
        form = CustomDeveloperCreationForm(form_data)
        if form.is_valid():
            developer = form.save(commit=False)

            similar_companies = User.objects.filter(company_identifier__iexact=developer.company_identifier)
            if similar_companies.exists():
                company = similar_companies.first()
                developer.name_company = company.name_company  # Устанавливаем name
                developer.save()
                return JsonResponse({'message': 'Регистрация прошла успешно'})
            else:
                messages.error(request, 'Нет похожих компаний. Напишите правильный идентификатор.')
        else:
            print("Form is not valid. Errors:", form.errors)
            messages.error(request, 'Форма заполнена неверно. Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomDeveloperCreationForm()
    return render(request, 'manager/registration.html', {'form': form})

@ensure_csrf_cookie
@csrf_exempt
def registration_manager(request):
    if request.method == 'POST':
        form = CustomManagerCreationForm(json.loads(request.body.decode('utf-8')), exclude_company_identifier=True)
        print(form)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.role = 2  # Устанавливаем статус "Компания"
            manager.company_identifier = str(uuid.uuid4())
            manager.save()
            login(request, manager)
            print("Manager saved successfully.")
            return redirect('company_dashboard')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = CustomManagerCreationForm(exclude_company_identifier=True)
    return render(request, 'manager/registration_manager.html', {'form': form})


@ensure_csrf_cookie
@csrf_exempt
def authentication(request):
    if request.method == 'POST':
        try:
            data = (json.loads(request.body.decode('utf-8')))
            username = data.get('username')
            password = data.get('password')

            # Проверяем, что логин и пароль были отправлены
            if username and password:
                # Аутентификация пользователя
                user = authenticate(username=username, password=password)

                # Если пользователь с таким логином и паролем существует
                if user is not None:
                    # Авторизуем пользователя
                    login(request, user)
                    # Возвращаем данные пользователя
                    user_data = [{
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'data_joined_to_work': user.data_joined_to_work,
                        'bin': user.bin,
                        'name_company': user.name_company,
                        'role': user.role,
                        'company_identifier': user.company_identifier,
                        # Добавьте другие данные пользователя, если нужно
                    }]
                    return JsonResponse(user_data, safe=False)
                else:
                    return JsonResponse({'error': 'Invalid username or password'}, status=400)
            else:
                return JsonResponse({'error': 'Username and password are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
