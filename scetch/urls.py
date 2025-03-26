from django.urls import path
from .views import home, queue_list, book_slot, status, status_date, delete_booking

urlpatterns = [
    path('', home,name='old_home'),
    path('queute_list/', queue_list, name='old_queute_list'),
    path('block_slots/', book_slot, name='old_block_slots'),
    path('status/', status, name='old_status'),
    path('book-slot/<int:slot_id>/', book_slot, name='old_book_slot'),
    path('all_slots/', status_date, name='old_all_slots'),
    path('delete_booking/<int:slot_id>/', delete_booking, name='old_delete_booking')
]

