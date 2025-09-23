from rest_framework import serializers
from .models import Attendance, Performance

class AttendanceSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'employee_id', 'employee', 'date', 'status']
        read_only_fields = ['employee']

class PerformanceSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Performance
        fields = ['id', 'employee_id', 'employee', 'rating', 'review_date', 'remarks']
        read_only_fields = ['employee']
