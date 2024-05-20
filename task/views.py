import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from task.models import *
from notifications.models import *

@csrf_exempt
@ensure_csrf_cookie
def create_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            required_fields = ['name_project', 'user', 'project_descriptions', 'project_date_start', 'project_date_end']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'success': False, 'error': f'Missing required field: {field}'}, status=400)

            project = Project.objects.create(
                name_project=data['name_project'],
                user_id=data['user'],
                project_descriptions=data['project_descriptions'],
                project_date_start=data['project_date_start'],
                project_date_end=data['project_date_end'],
                file_project=request.FILES.get('file_project')
            )
            if not ProjectMembership.objects.filter(user_id=data['user'], project_id=project.id).exists():
                # Если пользователя нет в проекте, создаем новую запись в ProjectMembership
                projectmember = ProjectMembership(
                    user_id=data['user'],
                    project_id=project.id,
                    role=5
                )
                projectmember.save()

            user_projects = Project.objects.filter(user=project.user)
            projects_data = []
            for project in user_projects:
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
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
                projects_data.append(project_data)

            return JsonResponse({'success': True, 'project_id': project.id, 'projects': projects_data})
        except KeyError as e:
            return JsonResponse({'success': False, 'error': f'Missing required parameter: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
@ensure_csrf_cookie
def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            task = Task.objects.create(
                name_task=data['name_task'],
                user_id=data['user'],
                project_id=data['project_id'],
                task_descriptions=data['task_descriptions'],
                task_date_start= data['task_date_start'],
                task_date_end = data['task_date_end'],
                task_priority=data['task_priority'],
                task_complexity=data['task_complexity'],
                file_task=request.FILES.get('file_task')
            )
            notifications = Notification.objects.create(
                user_id=data['user'],
                message=f'Вам назначена новая задача {data["name_task"]}',
            )

            if not ProjectMembership.objects.filter(user_id=data['user'], project_id=data['project_id']).exists():
                role_user = User.objects.get(id=data['user'],)
                projectmember = ProjectMembership(
                    user_id=data['user'],
                    project_id=data['project_id'],
                    role=role_user.role,
                )
                projectmember.save()

            user_projects = Project.objects.filter(user=data['teamlead_id'])
            projects_data = []
            for project in user_projects:
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
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
                projects_data.append(project_data)

            return JsonResponse({'success': True, 'project_id': project.id, 'projects': projects_data})
        except KeyError as e:
            return JsonResponse({'success': False, 'error': 'Missing required parameter: {}'.format(str(e))},status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred: {}'.format(str(e))}, status=400)

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
@ensure_csrf_cookie
def edit_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            if task_id:
                task = Task.objects.get(id=task_id)
                if 'name_task' in data:
                    task.name_task = data['name_task']
                if 'task_descriptions' in data:
                    task.task_descriptions = data['task_descriptions']
                if 'task_date_start' in data:
                    task.task_date_start = data['task_date_start']
                if 'task_date_end' in data:
                    task.task_date_end = data['task_date_end']
                if 'task_priority' in data:
                    task.task_priority = data['task_priority']
                if 'task_complexity' in data:
                    task.task_complexity = data['task_complexity']

                task.save()
                task_data = {
                    'task_id': task.id,
                    'name_task': task.name_task,
                    'task_descriptions': task.task_descriptions,
                    'task_date_start': task.task_date_start,
                    'task_date_end': task.task_date_end,
                    'task_priority': task.task_priority,
                    'task_complexity': task.task_complexity,
                }
                return JsonResponse({'success': 'Task updated successfully', 'task_data': task_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            if task_id:
                task = Task.objects.get(id=task_id)
                task.delete()
                return JsonResponse({'success': 'Task deleted successfully'})
            else:
                return JsonResponse({'error': 'Project ID not provided'}, status=400)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@ensure_csrf_cookie
def edit_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('project_id')
            if project_id:
                project = Project.objects.get(id=project_id)
                if 'name_project' in data:
                    project.name_task = data['name_project']
                if 'project_descriptions' in data:
                    project.task_descriptions = data['project_descriptions']
                if 'project_date_start' in data:
                    project.task_date_start = data['project_date_start']
                if 'project_date_end' in data:
                    project.task_date_end = data['project_date_end']

                project.save()
                project_data = {
                    'project_id': project.id,
                    'name_project': project.name_project,
                    'project_descriptions': project.project_descriptions,
                    'project_date_start': project.project_date_start,
                    'project_date_end': project.project_date_end,
                }
                return JsonResponse({'success': 'Task updated successfully', 'project_data': project_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            project_id = data.get('project')
            if project_id:
                project = Project.objects.get(id=project_id)
                project.delete()
                return JsonResponse({'success': 'Task deleted successfully'})
            else:
                return JsonResponse({'error': 'Project ID not provided'}, status=400)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@ensure_csrf_cookie
def send_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            task_id = data.get('task_id')
            task = Task.objects.get(id=task_id)
            task.task_status = 2
            task.save()
            return JsonResponse({'success': 'Task sent successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@ensure_csrf_cookie
def invite_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            task_id = data.get('task_id')
            task = Task.objects.get(id=task_id)
            task.id_tester = data['user']
            task.task_status = 2
            task.save()
            return JsonResponse({'success': 'Task sent successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@ensure_csrf_cookie
def send_task_analyst(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            task_id = data.get('task_id')
            task = Task.objects.get(id=task_id)
            task.task_status = 4
            task.save()
            return JsonResponse({'success': 'Task sent successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@ensure_csrf_cookie
def completed_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            task_id = data.get('task_id')
            task = Task.objects.get(id=task_id)
            task.task_status = 5
            task.save()
            return JsonResponse({'success': 'Task sent successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@ensure_csrf_cookie
def get_info_users(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            user_info = User.objects.get(id=data['id'])
            task_done = Task.objects.filter(user_id=data['id'], task_status=5)
            projects_amount = ProjectMembership.objects.filter(user_id=data['id'])
            info = {
                'task_done': len(task_done),
                'projects_amount': len(projects_amount),
                'username': user_info.username,
                'first_name': user_info.first_name,
                'last_name': user_info.last_name,
                'email': user_info.email,
                'data_joined_to_work': user_info.data_joined_to_work,
                'ava_image': user_info.ava_image.url if user_info.ava_image else None,
                'telegram': user_info.telegram,
                'role': user_info.role,
                'id': user_info.id,
                'phone_number': user_info.phone_number,
                'tasks': [],
            }
            print(info)
            tasks = Task.objects.filter(user_id=data['id'])
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
                info['tasks'].append(task_data)
            print(info)
            return JsonResponse(info, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@ensure_csrf_cookie
def calculate_user_kpi(request):
    data = json.loads(request.body)
    user_id = data.get('user_id')
    # Получить пользователя по user_id
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Рассчитать KPI пользователя
    kpi = calculate_user_kpi_value(user)

    # Получить данные о задачах пользователя
    tasks = Task.objects.filter(user=user).values('name_task', 'task_status', 'task_date_start', 'task_date_end')

    # Формирование JSON-объекта с данными
    response_data = {
        'kpi': kpi,
        'tasks': list(tasks)  # Преобразование QuerySet в список словарей
    }

    return JsonResponse(response_data)

def calculate_user_kpi_value(user):
    # Рассчитать общее количество единиц работы пользователя
    total_work_units = 0
    tasks = Task.objects.filter(user=user)
    for task in tasks:
        task_work_units = calculate_task_work_units(task)
        total_work_units += task_work_units

    # Рассчитать процент выполненной работы пользователя
    completed_work_units = 0
    for task in tasks:
        if task.task_status == 5:  # Предполагается, что статус 5 означает выполнение задачи
            task_work_units = calculate_task_work_units(task)
            completed_work_units += task_work_units

    if total_work_units == 0:
        return 0  # Вернуть 0, если у пользователя нет работы
    else:
        completion_rate = (completed_work_units / total_work_units) * 100
        return completion_rate

def calculate_task_work_units(task):
    # Словарь соответствия сложности задачи к количеству единиц работы
    complexity_units_mapping = {
        'Very Low': 1,
        'Low': 2,
        'Normal': 3,
        'Medium': 4,
        'High': 5,
    }

    # Словарь соответствия приоритета задачи к количеству единиц работы
    priority_units_mapping = {
        'Very Low': 1,
        'Low': 2,
        'Normal': 3,
        'Medium': 4,
        'High': 5,
    }
    task_work_units = (complexity_units_mapping[task.task_complexity] *
                       priority_units_mapping[task.task_priority])

    return task_work_units