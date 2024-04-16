import json

from django.http import JsonResponse

from notifications.models import Notification


def notifications(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notifications_user = Notification.object.get(user_id=data['user'], is_read=False)
            return JsonResponse(notifications_user, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Notification not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)