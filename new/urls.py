from django.urls import path
from new import views

urlpatterns = [
    path('', views.core, name='core'),
    path('bron/', views.schedule_view, name='schedule'),
    path('book-slot/<int:slot_id>/', views.book_slot, name='book_slot'),
]
