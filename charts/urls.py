from django.urls import path
from .views import employees_per_department, attendance_last_7_days

urlpatterns = [
    path('employees-per-department/', employees_per_department),
    path('attendance-last-7-days/', attendance_last_7_days),
]

from .views import dashboard
urlpatterns += [
    path('', dashboard, name='charts-dashboard'),
]
