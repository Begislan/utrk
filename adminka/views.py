from django.shortcuts import render
from scetch.models import Booking, QueueSlot, BookingArchive
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import validators
from django.utils.timezone import datetime


def staff_required(user):
    return user.is_staff  # Только сотрудники (админы, но не обязательно суперпользователи)


@user_passes_test(staff_required)
def adminka_home(request):
    bookings = Booking.objects.select_related('slot').all().order_by('-created_at')
    bookings_count = bookings.count()

    # filter date
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            bookings = bookings.filter(slot__date=filter_date)
        except ValueError:
            pass

    bookings = list(bookings)[:20]

    arhive_bookings = BookingArchive.objects.all()
    arhive_count = arhive_bookings.count()

    context = {
        'bookings': bookings,
        'bookings_count': bookings_count,
        'arhive_bookings': arhive_bookings,
        'arhive_count': arhive_count,
        'request': request,
    }

    return render(request, 'adminka/adminka_home.html', context)


@require_POST
@user_passes_test(staff_required)
def upload_video(request):
    try:
        booking_id = request.POST.get('booking_id')
        video_url = request.POST.get('video_url')

        if not booking_id or not video_url:
            return JsonResponse({'success': False, 'error': 'Не все поля заполнены'})

        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.video = video_url
        booking.save()

        return JsonResponse({'success': True})

    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Бронь не найдена'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
@user_passes_test(staff_required)
def delete_video(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.video = None
        booking.save()
        return JsonResponse({'success': True})
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Бронь не найдена'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
@user_passes_test(staff_required)
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


# arhive
@user_passes_test(staff_required)
def arhive_bookings(request):
    arhive_bookings = BookingArchive.objects.all()
    arhive_count = arhive_bookings.count()

    bookings = Booking.objects.all().order_by("-created_at")
    bookings_count = bookings.count()

    context = {
        'bookings': bookings,
        'bookings_count': bookings_count,
        'arhive_bookings': arhive_bookings,
        'arhive_count': arhive_count
    }
    return render(request, 'adminka/arhive_bookings.html', context)
