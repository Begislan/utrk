from django.urls import path
from adminka import views

urlpatterns = [
    path('', views.adminka_home, name='adminka_home'),
    path("upload-video/", views.upload_video, name="upload_video"),
    path('delete-video/<int:booking_id>/', views.delete_video, name='delete_video'),
    path('admin/delete-booking/<int:booking_id>/', views.admin_delete_booking, name='admin_delete_booking'),

]
