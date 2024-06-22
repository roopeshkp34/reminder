from django.urls import path
from . import views

app_name = "reminder"

urlpatterns = [
	path('', views.index, name="index"),
	path('send_reminder', views.send_notification, name="reminder"),
    path('not-available/<str:token>', views.not_available, name="NotAvailable")
    
]