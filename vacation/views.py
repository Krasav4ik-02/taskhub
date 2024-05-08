import json
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from datetime import date
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from notifications.models import Notification
from task.models import Task
from manager.models import User
from vacation.models import VacationRequest


@csrf_exempt
@ensure_csrf_cookie
def calculate_vacation_days(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            user_id = data.get('id')
            user = User.objects.get(id=user_id)
            managers = User.objects.filter(bin=user.bin, role = 1 )
            for manager in managers:
                manager_data = {
                    'manager_id': manager.id,
                }
                print(manager_data)
            if user.data_joined_to_work:
                info = {

                }
                years_worked = (date.today() - user.data_joined_to_work)
                years_worked_days = years_worked.days
                vacation_days = (years_worked.days / 365) * 24
                return JsonResponse({'years_worked_days': years_worked_days ,'vacation_days': vacation_days, 'manager_id': manager.id})
            else:
                return JsonResponse({'error': 'Дата начала работы не указана'})


        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь с указанным ID не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
@ensure_csrf_cookie
def submit_vacation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vacation_data = VacationRequest.objects.create(
            user_id=data['user'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            manager_id=data['manager_id'],
        )
        vacation_requests = VacationRequest.objects.filter(status='pending')


        vacation_tasks = Task.objects.filter(user__in=vacation_requests.values('user'), task_status__lt=5)

        if vacation_tasks.exists():
            for vacation_task in vacation_tasks:
                context = {
                    'task_id': vacation_task.id,
                    'task_name': vacation_task.name_task,
                }
            print(vacation_task)
            return JsonResponse({'Tasks': context}, safe=False)
        else:
            return JsonResponse({'message': 'No tasks found for users on vacation'}, status=200)

@csrf_exempt
@ensure_csrf_cookie
def vacations_for_manager(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            vacations= VacationRequest.objects.filter(user__bin=data['bin'])
            print(vacations)
            info = {
                'vacations': []
            }
            for vac in vacations:
                vacation={
                    'id_vacation' : vac.id,
                    'start_date' : vac.start_date,
                    'end_date' : vac.end_date,
                    'manager_id': vac.manager_id,
                    'status' : vac.status,
                    'user_id': vac.user_id,
                    'user_first_name': vac.user.first_name,
                    'user_last_name': vac.user.last_name,
                    'user_role': vac.user.role,
                    'user_ava_image': vac.user.ava_image.url if vac.user.ava_image else None,
                }
                print(vacation)
                info['vacations'].append(vacation)
            return JsonResponse(info, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'fff'}, status=400)