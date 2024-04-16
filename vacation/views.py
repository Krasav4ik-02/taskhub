import json

from django.http import JsonResponse
from django.shortcuts import render

from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

from notifications.models import Notification
from task.models import Task
from manager.models import User
from vacation.models import VacationRequest


@csrf_exempt
def calculate_vacation_days(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = User.objects.get(pk=user_id)
            current_year = datetime.now().year
            vacation_requests = VacationRequest.objects.filter(user=user, start_date__year=current_year)
            total_days_requested = sum((request.end_date - request.start_date).days + 1 for request in vacation_requests)
            remaining_days = user.vacation_days_per_year - total_days_requested
            return JsonResponse({'remaining_days': remaining_days}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)


@csrf_exempt
def submit_vacation_request(request):
    if request.method == 'POST':
        try:
            data = request.POST
            user_id = data.get('user_id')
            start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')

            user = User.objects.get(pk=user_id)
            vacation_request = VacationRequest.objects.create(user=user, start_date=start_date, end_date=end_date)

            # Определяем роль пользователя и рассылаем уведомления
            if user.role == 1:  # Если пользователь - менеджер
                # Рассылаем уведомления о заявке на отпуск всему персоналу или определенной группе
                pass  # Реализация рассылки уведомлений

            else:  # Если пользователь - не менеджер
                # Рассылаем уведомления о заявке на отпуск менеджеру
                managers = User.objects.filter(role=1)  # Получаем всех менеджеров
                for manager in managers:
                    # Отправляем уведомление о новой заявке на отпуск
                    pass  # Реализация отправки уведомлений

            return JsonResponse({'success': 'Заявка на отпуск успешно отправлена'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)

@csrf_exempt
def redistribute_tasks(request):
    if request.method == 'POST':
        try:
            data = request.POST
            user_id = data.get('user_id')

            user = User.objects.get(pk=user_id)
            tasks = Task.objects.filter(user=user, task_status=1)  # Получаем все задачи пользователя, находящиеся на рассмотрении

            # Реализация перераспределения задач по уровню сложности другим пользователям
            # Например, путем изменения полей user_id в объектах задач

            return JsonResponse({'success': 'Задачи успешно перераспределены'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
