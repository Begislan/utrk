from django.shortcuts import render
from scetch.models import Booking, QueueSlot
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect

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


def upload_video(request):
    if request.method == "POST" and request.FILES.get("video"):
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)
        booking.video = request.FILES["video"]
        booking.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def delete_video(request, booking_id):
    # Проверка на наличие прав для удаления
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)

        # Если у бронирования есть видео, удаляем его
        if booking.video:
            booking.video.delete()  # Удаляет видеофайл с диска
            booking.video = None  # Очищаем поле видео в модели
            booking.save()  # Сохраняем изменения в базе данных

        # Перенаправление на страницу с бронированиями после удаления
        return redirect('adminka_home')  # За

def admin_delete_booking(request, booking_id):
    # Проверка на наличие прав для удаления
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        # Перенаправление на страницу со списком бронирований после удаления
        return redirect('adminka_home')  # Замените 'bookings_list' на имя вашего URL для списка бронирований