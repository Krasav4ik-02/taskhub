import base64
import json
import re
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from task.models import *
from manager.models import *
from notifications.models import *


@ensure_csrf_cookie
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body.decode('utf-8'))
            print(form_data)
            required_fields = ['username', 'last_name', 'first_name', 'password1', 'password2', 'bin', 'role']

            for field in required_fields:
                if field not in form_data or not form_data[field]:  # Если поле отсутствует или пустое
                    return JsonResponse({'error': f'{field.capitalize()} is required'}, status=400)

            if form_data['password1'] != form_data['password2']:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)

            role = int(form_data['role'])

            valid_roles = [1, 2, 3, 4, 5, 6, 7, 8]
            if role not in valid_roles:
                return JsonResponse({'error': 'Invalid role'}, status=400)

            hashed_password = make_password(form_data['password1'])
            similar_companies = User.objects.filter(bin__iexact=form_data['bin'])
            if similar_companies.exists():
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
            else:
                return JsonResponse({'error': 'A company with such a bin does not exist'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
@ensure_csrf_cookie
def registration_manager(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode('utf-8'))
        print(form_data)
        required_fields = ['username', 'last_name', 'first_name', 'name_company', 'password1', 'password2', 'bin']
        for field in required_fields:
            if field not in form_data or not form_data[field]:  # Если поле отсутствует или пустое
                return JsonResponse({'error': f'{field.capitalize()} is required'}, status=400)

        if form_data['password1'] != form_data['password2']:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        hashed_password = make_password(form_data['password1'])
        similar_companies = User.objects.filter(bin__iexact=str(form_data['bin']))
        if similar_companies.exists():
            return JsonResponse({'error': 'A company with such a bin already exists'}, status=400)
        else:
            user = User.objects.create(
                username=form_data['username'],
                last_name=form_data['last_name'],
                first_name=form_data['first_name'],
                name_company=form_data['name_company'],
                password=hashed_password,
                bin=form_data['bin'],
                role=1
            )
            user.save()
            return JsonResponse({'message': 'Registration successful'})

    return JsonResponse({'message': 'Manager saved successfully'}, status=200)


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
                    return JsonResponse(user_data, safe=False)
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
            users = User.objects.filter(role=5, bin=data['bin'])
            notifications = Notification.objects.filter(user_id=data['id'], is_read=False)
            info = {
                'projects': [],
                'teamleads': [],
                'notifications': [],
            }
            for project in user_projects:
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
                    'project_descriptions': project.project_descriptions,
                    'project_date_start': project.project_date_start,
                    'project_date_end': project.project_date_end,
                    'users_in_project': [],
                    'files': [],
                    'tasks': [],
                }
                files = ProjectFile.objects.filter(project_id=project.id)
                for file in files:
                    project_data['files'].append(file.file_project.url if file.file_project.url else None)
                users_in_project = User.objects.filter(projectmembership__project=project)
                for developer in users_in_project:
                    developer_data = {
                        'id': developer.id,
                        'username': developer.username,
                        'role': developer.role,
                        'ava_image': developer.ava_image.url if developer.ava_image else None,
                    }
                    project_data['users_in_project'].append(developer_data)
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
                        'files': [],
                    }
                    files = TaskFile.objects.filter(task_id=task.id)
                    for file in files:
                        if file.file_task:
                            task_data['files'].append(file.file_task.url if file.file_task.url else None)
                        else:
                            task_data['files'].append(None)
                    project_data['tasks'].append(task_data)
                info['projects'].append(project_data)
            for notification in notifications:
                notification_data = {
                    'message': notification.message,
                    'time': notification.timestamp,
                }
                info['notifications'].append(notification_data)

            for teamleads in users:
                teamleads = {
                    'id': teamleads.id,
                    'username': teamleads.username,
                    'role': teamleads.role,
                    'bin': teamleads.bin,
                }
                info['teamleads'].append(teamleads)
        elif data['role'] == 1:
            users_company = User.objects.filter(bin=data['bin'], role__in=[2,3,4,5,6,7,8])
            notifications = Notification.objects.filter(user_id=data['id'], is_read=False)
            info = {
                'users': [],
                'projects': [],
                'notifications': [],
            }
            for users in users_company:
                user_company = {
                    'id': users.id,
                    'username': users.username,
                    'first_name': users.first_name,
                    'last_name': users.last_name,
                    'role': users.role,
                    'email': users.email,
                    'data_joined_to_work': users.data_joined_to_work,
                    'ava_image': users.ava_image.url if users.ava_image else None,
                    'bin': users.bin
                }
                info['users'].append(user_company)
            for notification in notifications:
                notification = {
                    'message': notification.message,
                    'time': notification.timestamp,
                }
                info['notifications'].append(notification)

        elif data['role'] == 5:
            user_projects = Project.objects.filter(user__bin=data['bin'], user__id=data['id'])
            users = User.objects.filter(role__in=[2, 3, 4], bin=data['bin'])
            notifications = Notification.objects.filter(user_id=data['id'], is_read=False)
            info = {
                'projects': [],
                'developers': [],
                'notifications': [],
            }
            for project in user_projects:
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
                    'project_descriptions': project.project_descriptions,
                    'project_date_start': project.project_date_start,
                    'project_date_end': project.project_date_end,
                    'tasks': [],
                    'users_in_project': [],
                    'files': [],
                }
                files = ProjectFile.objects.filter(project_id=project.id)
                for file in files:
                    project_data['files'].append(file.file_project.url if file.file_project.url else None)

                users_in_project = User.objects.filter(projectmembership__project=project)
                for developer in users_in_project:
                    developer_data = {
                        'id': developer.id,
                        'username': developer.username,
                        'role': developer.role,
                        'ava_image': developer.ava_image.url if developer.ava_image else None,
                    }
                    project_data['users_in_project'].append(developer_data)

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
                        'files': [],
                    }
                    files = TaskFile.objects.filter(task_id=task.id)
                    for file in files:
                        if file.file_task:
                            task_data['files'].append(file.file_task.url if file.file_task.url else None)
                        else:
                            task_data['files'].append(None)
                    project_data['tasks'].append(task_data)
                info['projects'].append(project_data)
            for developers in users:
                developers = {
                    'id': developers.id,
                    'username': developers.username,
                    'last_name': developers.last_name,
                    'first_name': developers.first_name,
                    'role': developers.role,
                    'bin': developers.bin,
                    'ava_image': developer.ava_image.url if developer.ava_image else None,
                }
                info['developers'].append(developers)
            for notification in notifications:
                notification_data = {
                    'message': notification.message,
                    'time': notification.timestamp,
                }
                info['notifications'].append(notification_data)
        elif data['role'] in [2, 3, 4]:
            projectmembers = ProjectMembership.objects.filter(user__id=data['id'])
            user_projects = Project.objects.filter(id__in=projectmembers.values_list('project_id', flat=True))
            users = User.objects.filter(role=6, bin=data['bin'])
            notifications = Notification.objects.filter(user_id=data['id'], is_read=False)
            info = {
                'projects': [],
                'testers': [],
                'notifications': [],
            }

            for project in user_projects:
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
                    'project_descriptions': project.project_descriptions,
                    'project_date_start': project.project_date_start,
                    'project_date_end': project.project_date_end,
                    'users_in_project': [],
                    'files': [],
                    'tasks': [],
                }
                files = ProjectFile.objects.filter(project_id=project.id)
                for file in files:
                    project_data['files'].append(file.file_project.url if file.file_project.url else None)
                users_in_project = User.objects.filter(projectmembership__project=project)
                for developer in users_in_project:
                    developer_data = {
                        'id': developer.id,
                        'username': developer.username,
                        'role': developer.role,
                        'ava_image': developer.ava_image.url if developer.ava_image else None,
                    }
                    project_data['users_in_project'].append(developer_data)
                tasks = Task.objects.filter(user__id=data['id'], project=project, task_status = 1)
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
                        'files': [],
                    }
                    files = TaskFile.objects.filter(task_id=task.id)
                    for file in files:
                        if file.file_task:
                            task_data['files'].append(file.file_task.url if file.file_task.url else None)
                        else:
                            task_data['files'].append(None)
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
            for notification in notifications:
                notification_data = {
                    'message': notification.message,
                    'time': notification.timestamp,
                }
                info['notifications'].append(notification_data)

        elif data['role'] == 6:
            users = User.objects.filter(bin = data['bin'])
            user_projects = Project.objects.filter(user__in= users)
            developers = User.objects.filter(role__in=[2, 3, 4], bin=data['bin'])
            analysts = User.objects.filter(role=7, bin=data['bin'])
            notifications = Notification.objects.filter(user_id=data['id'], is_read=False)
            print(data)
            info = {
                'projects': [],
                'developers': [],
                'analysts': [],
                'notifications': [],
            }
            for project in user_projects:
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
                    'project_descriptions': project.project_descriptions,
                    'project_date_start': project.project_date_start,
                    'project_date_end': project.project_date_end,
                    'users_in_project': [],
                    'files': [],
                    'tasks': [],
                    'tasks_tester': [],
                }
                files = ProjectFile.objects.filter(project_id=project.id)
                for file in files:
                    project_data['files'].append(file.file_project.url if file.file_project.url else None)
                users_in_project = User.objects.filter(projectmembership__project=project)
                for developer in users_in_project:
                    developer_data = {
                        'id': developer.id,
                        'username': developer.username,
                        'role': developer.role,
                        'ava_image': developer.ava_image.url if developer.ava_image else None,
                    }
                    project_data['users_in_project'].append(developer_data)
                tasks = Task.objects.filter(task_status = 2,project=project, id_tester = None)
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
                        'files': [],
                    }
                    files = TaskFile.objects.filter(task_id=task.id)
                    for file in files:
                        if file.file_task:
                            task_data['files'].append(file.file_task.url if file.file_task.url else None)
                        else:
                            task_data['files'].append(None)
                    project_data['tasks'].append(task_data)

                tasks = Task.objects.filter(task_status=2, project=project, id_tester=data['id'])
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
                        'id_tester': task.id_tester,
                        'files': [],
                    }
                    files = TaskFile.objects.filter(task_id=task.id)
                    for file in files:
                        if file.file_task:
                            task_data['files'].append(file.file_task.url if file.file_task.url else None)
                        else:
                            task_data['files'].append(None)
                    project_data['tasks_tester'].append(task_data)
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
            for notification in notifications:
                notification_data = {
                    'message': notification.message,
                    'time': notification.timestamp,
                }
                info['notifications'].append(notification_data)
        elif data['role'] == 7:
            user_projects = Project.objects.filter(user__bin=data['bin'])
            developers = User.objects.filter(role__in=[2, 3, 4], bin=data['bin'])
            teamleads = User.objects.filter(role=5, bin=data['bin'])
            notifications = Notification.objects.filter(user_id=data['id'], is_read=False)
            info = {
                'projects': [],
                'developers': [],
                'teamleads': [],
                'notifications': [],
            }
            for project in user_projects:
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
                    'project_descriptions': project.project_descriptions,
                    'project_date_start': project.project_date_start,
                    'project_date_end': project.project_date_end,
                    'users_in_project': [],
                    'files': [],
                    'tasks': [],
                }
                files = ProjectFile.objects.filter(project_id=project.id)
                for file in files:
                    project_data['files'].append(file.file_project.url if file.file_project.url else None)
                users_in_project = User.objects.filter(projectmembership__project=project)
                for developer in users_in_project:
                    developer_data = {
                        'id': developer.id,
                        'username': developer.username,
                        'role': developer.role,
                        'ava_image': developer.ava_image.url if developer.ava_image else None,
                    }
                    project_data['users_in_project'].append(developer_data)
                tasks = Task.objects.filter(project=project, task_status=4)
                for task in tasks:
                    task_data = {
                        'name_task': task.name_task,
                        'task_descriptions': task.task_descriptions,
                        'task_date_start': task.task_date_start,
                        'task_date_end': task.task_date_end,
                        'task_priority': task.task_priority,
                        'task_complexity': task.task_complexity,
                        'task_status': task.task_status,
                        'files': [],
                    }
                    files = TaskFile.objects.filter(task_id=task.id)
                    for file in files:
                        if file.file_task:
                            task_data['files'].append(file.file_task.url if file.file_task.url else None)
                        else:
                            task_data['files'].append(None)
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
            for notification in notifications:
                notification = {
                    'message': notifications.message,
                    'time': notifications.timestamp,
                }
                info['notifications'].append(notification)

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
                print(data)
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
                if 'ava_image' in data:
                    image_data = data['ava_image']
                    format, imgstr = image_data.split(';base64,')
                    img = ContentFile(base64.b64decode(imgstr), name='temp.' + re.search('image/(.*)', format).group(1))
                    if user.ava_image.name != 'avatars/default_avatar.png':
                        user.ava_image.delete()
                    user.ava_image.save('avatar.jpg', img, save=True)
                user.save()

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

                return JsonResponse({'success': 'Profile updated successfully', 'user_data': user_data})
            else:
                return JsonResponse({'error': 'User ID not provided'}, status=400)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
@ensure_csrf_cookie
def company_info(request):
    data = json.loads(request.body.decode('utf-8'))
    company = Company.objects.get(bin=data['bin'])
    name_comp = User.objects.get(bin=data['bin'])

    for comp in company:
        info = {
            'name_company': name_comp.name_company,
            'descriptions': comp.descriptions,
            'email': comp.email,
            'address': comp.address,
            'contact_phone': comp.contact_phone,
            'telegram': comp.telegram,
            'users': [],
        }
        users = User.objects.filter(bin=data['bin'])
        for user in users:
            user_info = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'ava_image': user.ava_image,
                'role': user.role,
            }
            info['users'].append(user_info)
    return JsonResponse(info)
