import base64
import json
import re
import uuid

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
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
                    user_data = {
                        'user': {
                            'email': user.email,
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'name_company': user.name_company,
                            'bin': user.bin,
                            'role': user.role,
                            'data_joined_to_work': user.data_joined_to_work,
                            'ava_image': user.ava_image.url if user.ava_image else None,
                            'city': user.city,
                            'telegram': user.telegram,
                            'country': user.country,
                            'phone_number': user.phone_number,
                        },
                    }
                    return JsonResponse(user_data , safe=False)
                else:
                    return JsonResponse({'error': 'Invalid username or password'}, status=400)
            else:
                return JsonResponse({'error': 'Username and password are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
@ensure_csrf_cookie
def dashboard(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data['role'] == 8:
            user_projects = Project.objects.filter(user__bin=data['bin'])
            users = User.objects.filter(role=5,bin=data['bin'])
            info = {
                'projects': [],
                'teamleads': [],
            }
            for project in user_projects:
                project_data = {
                        'project_id': project.id,
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
                info['projects'].append(project_data)
            for teamleads in users:
                teamleads = {
                    'id': teamleads.id,
                    'username': teamleads.username,
                    'role': teamleads.role,
                    'bin': teamleads.bin,
                }
                info['teamleads'].append(teamleads)

        elif data['role'] == 5:
            user_projects = Project.objects.filter(user__bin=data['bin'], user__id=data['id'])
            users = User.objects.filter(role__in=[2,3,4],bin=data['bin'])
            info = {
                'projects': [],
                'developers': [],
            }
            for project in user_projects:
                project_data = {
                        'project_id': project.id,
                        'name_project': project.name_project,
                        'project_descriptions': project.project_descriptions,
                        'project_date_start': project.project_date_start,
                        'project_date_end': project.project_date_end,
                        'tasks': [],
                    }

                tasks = Task.objects.filter(project=project)
                for task in tasks:
                    task_data = {
                        'task_id': task.id,
                        'name_task': task.name_task,
                        'task_descriptions': task.task_descriptions,
                        'task_date_start': task.task_date_start,
                        'task_date_end': task.task_date_end,
                        'task_priority': task.task_priority,
                        'task_complexity': task.task_complexity,
                        'task_status': task.task_status,
                    }
                    project_data['tasks'].append(task_data)
                info['projects'].append(project_data)
            for developers in users:
                developers = {
                    'id': developers.id,
                    'username': developers.username,
                    'role': developers.role,
                    'bin': developers.bin,
                }
                info['developers'].append(developers)

        elif data['role'] in [2,3,4]:
            projectmembers = ProjectMembership.objects.filter(user__id=data['id'])
            user_projects = Project.objects.filter(id__in=projectmembers.values_list('project_id', flat=True))
            users = User.objects.filter( role=6 , bin=data['bin'] )
            info = {
                'projects': [],
                'testers': [],
            }

            for project in user_projects:
                project_data = {
                        'project_id': project.id,
                        'name_project': project.name_project,
                        'project_descriptions': project.project_descriptions,
                        'project_date_start': project.project_date_start,
                        'project_date_end': project.project_date_end,
                        'tasks': [],
                    }

                tasks = Task.objects.filter(user__id=data['id'], project=project)
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
                info['projects'].append(project_data)
            for testers in users:
                testers = {
                    'id': testers.id,
                    'username': testers.username,
                    'role': testers.role,
                    'bin': testers.bin,
                }
                info['testers'].append(testers)

        elif data['role'] == 6:
            user_projects = Project.objects.filter(user__bin=data['bin'], user__id=data['id'])
            developers = User.objects.filter( role__in=[2,3,4] , bin=data['bin'] )
            analysts = User.objects.filter(role=7, bin=data['bin'] )
            info = {
                'projects': [],
                'developers': [],
                'analysts': [],
            }
            for project in user_projects:
                project_data = {
                        'project_id': project.id,
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
                info['projects'].append(project_data)
            for developer in developers:
                developer = {
                    'id': developer.id,
                    'username': developer.username,
                    'role': developer.role,
                    'bin': developer.bin,
                }
                info['developers'].append(developer)

            for analyst in analysts:
                analyst = {
                    'id': analyst.id,
                    'username': analyst.username,
                    'role': analyst.role,
                    'bin': analyst.bin,
                }
                info['analysts'].append(analyst)

        elif data['role'] == 7:
            user_projects = Project.objects.filter(user__bin=data['bin'], user__id=data['id'])
            developers = User.objects.filter( role__in=[2,3,4] , bin=data['bin'] )
            teamleads = User.objects.filter(role=5, bin=data['bin'] )
            info = {
                'projects': [],
                'developers': [],
                'teamleads': [],
            }
            for project in user_projects:
                project_data = {
                        'project_id': project.id,
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
                info['projects'].append(project_data)
            for developer in developers:
                developer = {
                    'id': developer.id,
                    'username': developer.username,
                    'role': developer.role,
                    'bin': developer.bin,
                }
                info['developers'].append(developer)
            for teamlead in teamleads:
                teamlead = {
                    'id': teamlead.id,
                    'username': teamlead.username,
                    'role': teamlead.role,
                    'bin': teamlead.bin,
                }
                info['teamleads'].append(teamlead)

        return JsonResponse(info, safe=False)


@csrf_exempt
@ensure_csrf_cookie
def edit_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        try:
            user_id = data.get('user')
            if user_id:
                user = User.objects.get(id=user_id)
                print(user)

                # Обновляем поля профиля, если они были переданы в запросе
                if 'username' in data:
                    user.username = data['username']
                if 'first_name' in data:
                    user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                if 'name_company' in data:
                    user.name_company = data['name_company']
                if 'bin' in data:
                    user.bin = data['bin']
                if 'role' in data:
                    user.role = data['role']
                if 'data_joined_to_work' in data:
                    user.data_joined_to_work = data['data_joined_to_work']
                if 'email' in data:
                    user.email = data['email']
                if 'city' in data:
                    user.city = data['city']
                if 'telegram' in data:
                    user.telegram = data['telegram']
                if 'country' in data:
                    user.country = data['country']
                if 'phone_number' in data:
                    user.phone_number = data['phone_number']
                # Обновляем изображение профиля, если оно было передано в запросе
                if 'ava_image' in data:
                    # Получаем данные изображения
                    image_data = data['ava_image']
                    # Извлекаем base64-часть изображения
                    format, imgstr = image_data.split(';base64,')
                    # Создаем изображение из base64-строки
                    img = ContentFile(base64.b64decode(imgstr), name='temp.' + re.search('image/(.*)', format).group(1))

                    if user.ava_image:
                        user.ava_image.delete()

                    user.ava_image.save('avatar.jpg', img, save=True)

                user.save()

                # Формируем словарь с данными профиля пользователя
                user_data = {
                    'email': user.email,
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'name_company': user.name_company,
                    'bin': user.bin,
                    'role': user.role,
                    'data_joined_to_work': user.data_joined_to_work,
                    'ava_image': user.ava_image.url if user.ava_image else None,
                    'city': user.city,
                    'telegram': user.telegram,
                    'country': user.country,
                    'phone_number': user.phone_number,
                }

                # Отправляем данные профиля пользователя в виде JSON-ответа
                return JsonResponse({'success': 'Profile updated successfully', 'user_data': user_data})
            else:
                return JsonResponse({'error': 'User ID not provided'}, status=400)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)