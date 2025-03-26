# views.py
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from scetch.models import QueueSlot, Booking
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


def core(request):
    return render(request, 'new/home.html')
@login_required
def schedule_view(request):
    # Обработка выбора даты
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.localdate()
    else:
        selected_date = timezone.localdate()

    # Обработка удаления бронирования (POST запрос)
    if request.method == 'POST' and 'delete_booking' in request.POST:
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        slot = booking.slot
        booking.delete()
        slot.is_booked = False
        slot.save()
        return redirect('schedule')

    # Определяем диапазон дат (сегодня + 31 день)
    start_date = timezone.localdate()
    end_date = start_date + timedelta(days=31)
    # Определяем текущую дату (без времени)
    today = timezone.localdate()

    # Получаем все существующие даты в этом диапазоне
    existing_dates = set(QueueSlot.objects.filter(
        date__range=[start_date, end_date]
    ).values_list('date', flat=True).distinct())

    # Создаем список всех дат в диапазоне
    all_dates = [start_date + timedelta(days=i) for i in range(32)]  # 31 день + сегодня

    # Находим даты, для которых нужно создать слоты
    dates_to_create = [date for date in all_dates if date not in existing_dates]

    # Создаем слоты для недостающих дат
    if dates_to_create:
        times = [
            {'start': '09:00', 'end': '09:30'},
            {'start': '09:30', 'end': '10:00'},
            {'start': '10:00', 'end': '10:30'},
            {'start': '10:30', 'end': '11:00'},
            {'start': '11:00', 'end': '11:30'},
            {'start': '11:30', 'end': '12:00'},
            {'start': '13:00', 'end': '13:30'},
            {'start': '13:30', 'end': '14:00'},
            {'start': '14:00', 'end': '14:30'},
            {'start': '14:30', 'end': '15:00'},
            {'start': '15:00', 'end': '15:30'},
            {'start': '15:30', 'end': '16:00'},
            {'start': '16:00', 'end': '16:30'},
            {'start': '16:30', 'end': '17:00'},
            {'start': '17:00', 'end': '17:30'},
            {'start': '17:30', 'end': '18:00'}
        ]

        slots_to_create = []
        for date in dates_to_create:
            for time in times:
                slots_to_create.append(
                    QueueSlot(
                        date=date,
                        start_time=time['start'],
                        end_time=time['end']
                    )
                )

        QueueSlot.objects.bulk_create(slots_to_create)

    # Получаем все слоты и бронирования для диапазона
    slots = QueueSlot.objects.filter(date__gte=today, date__lte=end_date).order_by('date', 'start_time')
    bookings = Booking.objects.filter(slot__date__range=[start_date, end_date]).select_related('user', 'slot')

    # Группировка данных
    week_dates = [start_date + timedelta(days=i) for i in range(32)]  # 31 день + сегодня
    time_slots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00",
                  "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
                  "16:00", "16:30", "17:00", "17:30"]

    # Создаем структуру данных для шаблона
    schedule_data = []
    for time in time_slots:
        row = {'time': time, 'days': []}
        for date in week_dates:
            day_slots = []
            for slot in slots.filter(date=date, start_time__startswith=time):
                booking = bookings.filter(slot=slot).first()
                day_slots.append({
                    'slot': slot,
                    'booking': booking,
                    'is_owned': booking.user == request.user if booking else False
                })
            row['days'].append(day_slots)
        schedule_data.append(row)

    context = {
        'selected_date': selected_date,
        'week_dates': week_dates,
        'schedule_data': schedule_data,
        'time_slots': time_slots,
    }

    return render(request, 'new/schedule.html', context)


@login_required
@csrf_exempt  # Временно отключаем CSRF для AJAX (для теста)
@require_POST
def book_slot(request, slot_id):
    slot = get_object_or_404(QueueSlot, id=slot_id)

    if slot.is_booked:
        return JsonResponse({"success": False, "error": "Этот слот уже занят"}, status=400)

    # Проверяем, не имеет ли пользователь уже бронь на это время
    existing_booking = Booking.objects.filter(
        user=request.user,
        slot__date=slot.date,
        slot__start_time=slot.start_time
    ).exists()

    if existing_booking:
        return JsonResponse({"success": False, "error": "У вас уже есть бронь на это время"}, status=400)

    Booking.objects.create(user=request.user, slot=slot)
    slot.is_booked = True
    slot.save()

    return JsonResponse({
        "success": True,
        "message": "Вы успешно записаны!",
        "booking_id": Booking.objects.get(slot=slot).id
    })