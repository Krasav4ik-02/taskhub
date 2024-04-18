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
            user_id = data.get('user_id')  # Проверьте, что user_id присутствует в данных
            user = User.objects.get(id=user_id)  # Получите объект пользователя по его ID

            # Проверяем, что у пользователя есть дата начала работы
            if user.data_joined_to_work:
                info = {

                }
                years_worked = (date.today() - user.data_joined_to_work)  # Считаем стаж работы в годах
                vacation_days = (years_worked.days / 365) * 24  # Подсчитываем отпускные дни
                return JsonResponse({'vacation_days': vacation_days})
            else:
                return JsonResponse({'error': 'Дата начала работы не указана'})

            # Вернуть результат в формате JSON

        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь с указанным ID не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  # Вернуть сообщение об ошибке в случае исключения
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)  # Вернуть сообщение об ошибке, если метод не POST

@csrf_exempt
@ensure_csrf_cookie
def create_vacation_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not all([user_id, start_date, end_date]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            user = User.objects.get(id=user_id)

            # Проверка наличия задач у пользователя
            if user.role == [2,3,4]:
                tasks_exist = Task.objects.filter(user__id=user, task_status=1).exists()

                if tasks_exist:
                    # Если есть задачи, перераспределение задач на других коллег
                    tasks = Task.objects.filter(user__id=user)
                    for task in tasks:
                        task_data = {
                            'task_id': task.id,
                            'task_name': task.task_name,
                        }
                    return JsonResponse({'error': 'You have pending tasks. Please wait for their distribution.'}, status=400)
                else:
                    # Если задач нет, создаем новую заявку на отпуск
                    with transaction.atomic():
                        # Используем транзакцию для обеспечения целостности данных
                        vacation_request = VacationRequest.objects.create(
                            user=user,
                            start_date=start_date,
                            end_date=end_date
                        )

                        # Отправляем уведомление менеджеру о новой заявке на отпуск
                        # (здесь нужно добавить логику отправки уведомления)

                    return JsonResponse({'success': 'Vacation request created successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return HttpResponseNotAllowed(['POST'])
