from datetime import timedelta
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import QueueSlot, Booking
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def home(request):
    return render(request, 'home/home.html')

@require_POST
def book_slot(request, slot_id):
    if not request.user.is_authenticated:
        return JsonResponse({"redirect": "/accounts/login/"}, status=401)  # JSON-ответ для AJAX

    slot = get_object_or_404(QueueSlot, id=slot_id)

    if slot.is_booked:
        return JsonResponse({"error": "Этот слот уже занят"}, status=400)

    # Бронируем слот
    Booking.objects.create(user=request.user, slot=slot)
    slot.is_booked = True
    slot.save()

    return JsonResponse({"message": "Вы успешно записаны!"})

def queue_list(request):
    date_str = request.GET.get('date', timezone.now().date().strftime('%Y-%m-%d'))

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        date = timezone.now().date()

    is_exist = QueueSlot.objects.filter(date=date).exists()

    if not is_exist:
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

        slots = [QueueSlot(date=date, start_time=data['start'], end_time=data['end']) for data in times]
        QueueSlot.objects.bulk_create(slots)

    slots = QueueSlot.objects.filter(date=date)
    date = timezone.now().date()
    return render(request, "home/queue.html", {'selected_date': date, 'slots': slots})

@login_required
def status(request):
    books = Booking.objects.filter(user=request.user)

    context = {
        'book': books
    }

    return render(request, 'home/status.html', context)

@login_required
def delete_booking(request, slot_id):
    booking = Booking.objects.get(id=slot_id)
    slot = booking.slot
    if request.method == 'POST':
        booking.delete()
        slot.is_booked = False
        slot.save()
        return redirect('old_status')
    return render(request, 'home/delete_booking.html', {'booking': booking})

@login_required
def status_date(request):
    today = timezone.localdate()
    start_date = today - timedelta(days=today.weekday())  # Понедельник текущей недели
    end_date = start_date + timedelta(days=6)  # Воскресенье текущей недели

    books = Booking.objects.filter(slot__date__range=[start_date, end_date]).order_by("slot__date", "slot__start_time")

    # Группируем бронирования по дате
    grouped_books = {}
    for booking in books:
        date = booking.slot.date
        if date not in grouped_books:
            grouped_books[date] = []
        grouped_books[date].append(booking)

    return render(request, 'home/status_date.html', {
        "grouped_books": grouped_books,
        "week_dates": [start_date + timedelta(days=i) for i in range(7)]
    })
