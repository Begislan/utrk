from django.urls import path
from adminka import views

urlpatterns = [
    path('', views.adminka_home, name='adminka_home'),
    path('add-video-url/', views.upload_video, name='upload_video'),
    path('<int:booking_id>/delete-video/', views.delete_video, name='delete_video'),
    path('delete-booking/<int:booking_id>/', views.admin_delete_booking, name='admin_delete_booking'),
    #arhive
    path('arhive_videos/', views.arhive_bookings, name='arhive_videos')

]
