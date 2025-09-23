from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from employees.models import Department, Employee
from attendance.models import Attendance

@api_view(['GET'])
@permission_classes([AllowAny])
def employees_per_department(request):
    # Use the correct reverse name from Department to Employee: "employees"
    data = (
        Department.objects
        .annotate(total=Count('employees'))  # <— key change: 'employees', not 'employee'
        .values('name', 'total')
        .order_by('name')
    )
    labels = [row['name'] for row in data]
    values = [row['total'] for row in data]
    return Response({'labels': labels, 'values': values})

@api_view(['GET'])
@permission_classes([AllowAny])
def attendance_last_7_days(request):
    today = timezone.now().date()
    start = today - timedelta(days=6)
    qs = (
        Attendance.objects
        .filter(date__range=[start, today])
        .values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )
    labels = [row['status'] for row in qs]
    values = [row['total'] for row in qs]
    return Response({'labels': labels, 'values': values})

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard(request):
    return render(request, 'charts/dashboard.html')
