from django.urls import path
from .views import home, queue_list, book_slot, status, status_date, delete_booking

urlpatterns = [
    path('', home,name='home'),
    path('queute_list/', queue_list, name='queute_list'),
    path('block_slots/', book_slot, name='block_slots'),
    path('status/', status, name='status'),
    path('book-slot/<int:slot_id>/', book_slot, name='book_slot'),
    path('all_slots/', status_date, name='all_slots'),
    path('delete_booking/<int:slot_id>/', delete_booking, name='delete_booking')
]

