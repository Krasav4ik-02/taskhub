import json

from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from task.models import *

@csrf_exempt
@ensure_csrf_cookie
def create_project(request):
    if request.method == 'POST':
        try:
            # Получаем данные из тела запроса
            data = json.loads(request.body)
            # users = User.objects.filter(bin=bin.user, role=5)
            # for user in users:
            #     users_data={
            #         'id': user.id,
            #         'username': user.username
            #     }
            # return JsonResponse(users_data)

            # Создаем проект
            project = Project.objects.create(
                name_project=data['name_project'],
                user_id=data['user'],
                project_descriptions=data['project_descriptions'],
                project_date_start=data['project_date_start'],
                project_date_end=data['project_date_end']
            )
            project.save()

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

            return JsonResponse({'success': True, 'project_id': project.id, 'projects': projects_data})
        except Exception as e:
            # Если произошла ошибка, возвращаем сообщение об ошибке
            return JsonResponse({'success': False, 'error': str(e)})

    # Если запрос не является POST, возвращаем ошибку метода
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)