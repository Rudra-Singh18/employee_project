from rest_framework import viewsets, filters
from .models import Attendance, Performance
from .serializers import AttendanceSerializer, PerformanceSerializer
from employees.models import Employee
from rest_framework.response import Response
from rest_framework import status

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee').all().order_by('-date')
    serializer_class = AttendanceSerializer
    filterset_fields = ['status', 'date', 'employee']
    ordering_fields = ['date', 'id']


    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'detail': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, employee)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, employee):
        serializer.save(employee=employee)

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related('employee').all().order_by('-review_date')
    serializer_class = PerformanceSerializer
    filterset_fields = ['rating', 'review_date', 'employee']
    ordering_fields = ['review_date', 'rating', 'id']


    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'detail': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, employee)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, employee):
        serializer.save(employee=employee)
