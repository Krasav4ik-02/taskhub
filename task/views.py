import json
from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.utils.timezone import make_aware
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from task.models import *

@csrf_exempt
@ensure_csrf_cookie
def create_project(request):
    if request.method == 'POST':
            data = json.loads(request.body)

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
            )

            # Возвращаем успешный ответ с данными о проектах пользователя
            user_projects = Project.objects.filter(user=project.user)
            projects_data = []
            for project in user_projects:
                project_data = {
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

            return JsonResponse({'success': True, 'projects_data': projects_data})

@csrf_exempt
@ensure_csrf_cookie
def create_task(request):
    if request.method == 'POST':
        try:
            # Получаем данные из тела запроса
            data = json.loads(request.body)
            print(data)
            task = Task.objects.create(
                name_task=data['name_task'],
                user_id=data['user'],
                project_id=data['project_id'],
                task_descriptions=data['task_descriptions'],
                task_date_start=make_aware(datetime.strptime(data['task_date_start'], '%Y-%m-%dT%H:%M:%S')),
                task_date_end = make_aware(datetime.strptime(data['task_date_end'], '%Y-%m-%dT%H:%M:%S')),
                task_priority=data['task_priority'],
                task_complexity=data['task_complexity'],
            )
            task.task_status = 1
            task.save()

            user_projects = Project.objects.filter(user=task.user)
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
        except Exception as e:
            # Если произошла ошибка, возвращаем сообщение об ошибке
            return JsonResponse({'success': False, 'error': str(e)})

    # # Если запрос не является POST, возвращаем ошибку метода
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

