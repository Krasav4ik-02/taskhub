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
            user = User.objects.get(id=data['id'])
            managers = User.objects.get(bin=user.bin, role = 1 )
            vacations = VacationRequest.objects.filter(user_id = data['id'], status=2)
            vacations_used_up = VacationRequest.objects.filter(user_id = data['id'], status=2, start_date__year= date.today().year)
            if user.data_joined_to_work:
                years_worked = (date.today() - user.data_joined_to_work)
                print(years_worked.days)
                vacation_days = int(((years_worked.days / 365) * 24))
                mers = 0
                bmw = 0
                for vacation_used_up in vacations_used_up:
                    vacat = vacation_used_up.end_date - vacation_used_up.start_date
                    bmw += vacat.days
                for vacation in vacations:
                    vacat = vacation.end_date - vacation.start_date
                    mers += vacat.days

                vacation_requests = VacationRequest.objects.filter(user_id=data['id'])
                info = {
                    'manager_id': managers.id,
                    'date_joined_to_work': user.data_joined_to_work,
                    'balans': vacation_days-mers,
                    'used_up': vacation_days-bmw,
                    'vacation_request': [],
                }
                for vacation_request in vacation_requests:
                    days_vacation = vacation_request.end_date - vacation_request.start_date
                    vacation_request_data = {
                        'id_vacation': vacation_request.id,
                        'start_date': vacation_request.start_date,
                        'end_date': vacation_request.end_date,
                        'type_vacation': vacation_request.type_vacation,
                        'comments': vacation_request.comments,
                        'date': vacation_request.date,
                        'status': vacation_request.status,
                        'days': days_vacation.days,
                    }
                    info['vacation_request'].append(vacation_request_data)
                print(info)
                return JsonResponse(info, safe=False)
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
def apply_vacation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        vacation = VacationRequest.objects.get(id = data['id_vacation'])
        vacation.status = 2
        vacation.save()
        vacations = VacationRequest.objects.filter(user__bin=data['bin'], status=1)
        info = {
            'vacations': []
        }
        for vac in vacations:
            vacation = {
                'id_vacation': vac.id,
                'start_date': vac.start_date,
                'end_date': vac.end_date,
                'manager_id': vac.manager_id,
                'status': vac.status,
                'type_vacation': vac.type_vacation,
                'comments': vac.comments,
                'date': vac.date,
                'user_id': vac.user_id,
                'user_first_name': vac.user.first_name,
                'user_last_name': vac.user.last_name,
                'user_role': vac.user.role,
                'user_ava_image': vac.user.ava_image.url if vac.user.ava_image else None,
            }
            print(vacation)
            info['vacations'].append(vacation)
        return JsonResponse(info, safe=False)


@csrf_exempt
@ensure_csrf_cookie
def reject_vacation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        vacation = VacationRequest.objects.get(id = data['id_vacation'])
        vacation.status = 3
        vacation.save()
        vacations = VacationRequest.objects.filter(user__bin=data['bin'], status=1)
        info = {
            'vacations': []
        }
        for vac in vacations:
            vacation = {
                'id_vacation': vac.id,
                'start_date': vac.start_date,
                'end_date': vac.end_date,
                'manager_id': vac.manager_id,
                'status': vac.status,
                'type_vacation': vac.type_vacation,
                'comments': vac.comments,
                'date': vac.date,
                'user_id': vac.user_id,
                'user_first_name': vac.user.first_name,
                'user_last_name': vac.user.last_name,
                'user_role': vac.user.role,
                'user_ava_image': vac.user.ava_image.url if vac.user.ava_image else None,
            }
            print(vacation)
            info['vacations'].append(vacation)
        return JsonResponse(info, safe=False)

@csrf_exempt
@ensure_csrf_cookie
def submit_vacation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vacation_data = VacationRequest.objects.create(
            user_id=data['id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            manager_id=data['manager_id'],
            comments = data['comments'],
            date = date.today(),
            type_vacation = data['type_vacation']
        )

        vacation_tasks = Task.objects.filter(user_id=data['id'], task_status__lt=5)
        print(vacation_tasks)
        for vacation_task in vacation_tasks:
            vacation_task.task_vacation_status = True
            vacation_task.save()

        user = User.objects.get(id=data['id'])
        managers = User.objects.get(bin=user.bin, role=1)
        vacations = VacationRequest.objects.filter(user_id=data['id'], status=2)
        vacations_used_up = VacationRequest.objects.filter(user_id=data['id'], status=2,
                                                           start_date__year=date.today().year)
        if user.data_joined_to_work:
            years_worked = (date.today() - user.data_joined_to_work)
            print(years_worked.days)
            vacation_days = int(((years_worked.days / 365) * 24))
            mers = 0
            bmw = 0
            for vacation_used_up in vacations_used_up:
                vacat = vacation_used_up.end_date - vacation_used_up.start_date
                bmw += vacat.days
            for vacation in vacations:
                vacat = vacation.end_date - vacation.start_date
                mers += vacat.days
        vacation_requests = VacationRequest.objects.filter(user_id= data['id'])
        info = {
            'manager_id': managers.id,
            'date_joined_to_work': user.data_joined_to_work,
            'balans': vacation_days - mers,
            'used_up': vacation_days - bmw,
            'vacation_request': [],
        }
        for vacation_request in vacation_requests:
            days_vacation = vacation_request.end_date - vacation_request.start_date
            vacation_request_data = {
                'id_vacation': vacation_request.id,
                'start_date': vacation_request.start_date,
                'end_date': vacation_request.end_date,
                'type_vacation': vacation_request.type_vacation,
                'comments': vacation_request.comments,
                'date': vacation_request.date,
                'status': vacation_request.status,
                'days': days_vacation.days,
            }
            info['vacation_request'].append(vacation_request_data)
        return JsonResponse(info, safe=False)
    else:
        return JsonResponse({'message': 'No tasks found for users on vacation'}, status=200)

@csrf_exempt
@ensure_csrf_cookie
def vacations_for_manager(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vacations= VacationRequest.objects.filter(user__bin=data['bin'], status = 1)
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
                    'type_vacation': vac.type_vacation,
                    'comments': vac.comments,
                    'date': vac.date,
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

@csrf_exempt
@ensure_csrf_cookie
def vacations_for_manager_apply(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vacations= VacationRequest.objects.filter(user__bin=data['bin'], status = 2)
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
                    'type_vacation': vac.type_vacation,
                    'comments': vac.comments,
                    'date': vac.date,
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

@csrf_exempt
@ensure_csrf_cookie
def vacations_for_manager_reject(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vacations= VacationRequest.objects.filter(user__bin=data['bin'], status = 3)
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
                    'type_vacation': vac.type_vacation,
                    'comments': vac.comments,
                    'date': vac.date,
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

@csrf_exempt
@ensure_csrf_cookie
def vacation_tasks(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tasks = Task.objects.filter(user__bin=data['bin'], task_vacation_status = True)
            task_massiv = []
            for task in tasks:
                task_data = {
                    'user_id': task.user_id,
                    'name_task': task.name_task,
                    'user_ava_image': task.user.ava_image.url if task.user.ava_image else None,
                    'task_descriptions': task.task_descriptions,
                    'task_date_start': task.task_date_start,
                    'task_date_end': task.task_date_end,
                    'task_priority': task.task_priority,
                    'task_complexity': task.task_complexity,
                    'task_status': task.task_status,
                }
                task_massiv.append(task_data)
            return JsonResponse(task_massiv, safe=False)
        except Exception as e:
            return JsonResponse({'error': 'fff'}, status=400)