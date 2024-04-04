import json
import uuid

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from manager.models import *
from task.models import *
from manager.models import *

@ensure_csrf_cookie
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body.decode('utf-8'))
            print(form_data)
            # Check if required fields are present
            required_fields = ['username', 'last_name', 'first_name', 'password1', 'password2', 'bin', 'role']
            for field in required_fields:
                if field not in form_data:
                    return JsonResponse({'error': f'{field.capitalize()} is required'}, status=400)

            # Check if passwords match
            if form_data['password1'] != form_data['password2']:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)

            # Convert role to integer
            role = int(form_data['role'])

            # Check if role is valid
            valid_roles = [1, 2, 3, 4, 5, 6, 7, 8]
            if role not in valid_roles:
                return JsonResponse({'error': 'Invalid role'}, status=400)

            # Hash the password
            hashed_password = make_password(form_data['password1'])

            # Create the user
            user = User.objects.create(
                username=form_data['username'],
                last_name=form_data['last_name'],
                first_name=form_data['first_name'],
                name_company=form_data.get('name_company', ''),  # Проверяем наличие ключа
                password=hashed_password,
                bin=form_data['bin'],
                role=role
            )

            similar_companies = User.objects.filter(bin__iexact=user.bin)
            if similar_companies.exists():
                company = similar_companies.first()
                user.name_company = company.name_company  # Устанавливаем name
                user.save()
            return JsonResponse({'message': 'Registration successful'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return HttpResponseNotAllowed(['POST'])

@ensure_csrf_cookie
@csrf_exempt
def registration_manager(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode('utf-8'))
        print(form_data)
        # Check if required fields are present
        required_fields = ['username', 'last_name', 'first_name', 'name_company', 'password1', 'password2', 'bin','role']
        for field in required_fields:
            if field not in form_data:
                return JsonResponse({'error': f'{field.capitalize()} is required'}, status=400)

        # Check if passwords match
        if form_data['password1'] != form_data['password2']:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Hash the password
        hashed_password = make_password(form_data['password1'])

        # Create the user
        user = User.objects.create(
            username=form_data['username'],
            last_name=form_data['last_name'],
            first_name=form_data['first_name'],
            name_company=form_data['name_company'],
            password=hashed_password,
            bin=form_data['bin']
        )

        # Set role and save manager
        manager = user
        manager.role = 1  # Set role to "Company"
        manager.save()

        # Log in the manager and redirect
        login(request, manager)
        print("Manager saved successfully.")

@csrf_exempt
@ensure_csrf_cookie
def authentication(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    user_projects = Project.objects.filter(user=user)
                    user_data = {
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'data_joined_to_work': user.data_joined_to_work,
                            'bin': user.bin,
                            'name_company': user.name_company,
                            'role': user.role,
                        },
                        'projects': [],
                        'teamleads': [],
                    }
                    users = User.objects.filter(role=5, bin=user.bin)
                    for teamlead in users:
                        teamlead_data = {
                            'id': teamlead.id,
                            'username': teamlead.username,
                            'role': teamlead.role,
                            'bin' : teamlead.bin
                        }
                    user_data['projects'].append(teamlead_data)

                    for project in user_projects:
                        project_data = {
                            'name_project': project.name_project,
                            'project_descriptions': project.project_descriptions,
                            'project_date_start': project.project_date_start,
                            'project_date_end': project.project_date_end,
                            'tasks': [],
                        }
                        tasks = Task.objects.filter(project=project)
                        for task in tasks:
                            task_data = {
                                'name_task': task.name_task,
                                'task_descriptions': task.task_descriptions,
                                'task_date_start': task.task_date_start,
                                'task_date_end': task.task_date_end,
                                'task_priority': task.task_priority,
                                'task_complexity': task.task_complexity,
                                'task_status': task.task_status,
                            }

                            project_data['tasks'].append(task_data)
                        user_data['projects'].append(project_data)

                    return JsonResponse(user_data , safe=False)
                else:
                    return JsonResponse({'error': 'Invalid username or password'}, status=400)
            else:
                return JsonResponse({'error': 'Username and password are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

