from django.shortcuts import render
from scetch.models import Booking, QueueSlot
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from scetch.models import BookingArchive
import json

def staff_required(user):
    return user.is_staff  # Только сотрудники (админы, но не обязательно суперпользователи)


@user_passes_test(staff_required)
def adminka_home(request):
    date_filter = request.GET.get("date")
    bookings = Booking.objects.all().order_by("-created_at")
    bookings_count = bookings.count()

    if date_filter:
        bookings = bookings.filter(created_at__date=date_filter)

    context = {
        'bookings': bookings,
        'bookings_count': bookings_count
    }

    return render(request, 'adminka/adminka_home.html', context)


# def upload_video(request):
#     if request.method == "POST" and request.FILES.get("video"):
#         booking_id = request.POST.get("booking_id")
#         booking = get_object_or_404(Booking, id=booking_id)
#         booking.video = request.FILES["video"]
#         booking.save()
#         return JsonResponse({"success": True})
#     return JsonResponse({"success": False}, status=400)


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from scetch.models import Booking
import validators


@require_POST
def upload_video(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id)

        # Получаем URL видео из запроса
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body)
            video_url = data.get('video')
        else:
            video_url = request.POST.get('video')

        # Валидация
        if not video_url:
            return JsonResponse({'success': False, 'error': 'URL видео не указан'}, status=400)

        video_url = video_url.strip()
        if not validators.url(video_url):
            return JsonResponse({'success': False, 'error': 'Некорректный URL видео'}, status=400)

        # Сохраняем URL
        booking.video = video_url
        booking.save()

        return JsonResponse({
            'success': True,
            'message': 'Видео успешно сохранено',
            'video_url': booking.video
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def delete_video(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)

        # Просто очищаем поле video (так как это URL, а не файл)
        booking.video = None
        booking.save()

        # Возвращаем JSON для AJAX или делаем редирект
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('adminka_home')

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

@require_POST
def admin_delete_booking(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id)

        # Получаем комментарий из POST-данных
        delete_comment = request.POST.get('delete_comment', '')

        # Создаем архивную запись
 # with transaction.atomic():
        slot = booking.slot
        slot.is_booked = False
        slot.save()

        BookingArchive.objects.create(
            original_id=booking.id,
            user=booking.user,
            slot=booking.slot,
            created_at=booking.created_at,
            video=booking.video,
            delete_comment=delete_comment
        )
        booking.delete()

        return JsonResponse({
            'success': True,
            'message': 'Бронирование успешно перемещено в архив'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)