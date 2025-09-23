from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from employees.models import Department, Employee
from attendance.models import Attendance, Performance
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with departments, employees, attendance, and performance data"

    def add_arguments(self, parser):
        parser.add_argument('--employees', type=int, default=40, help='Number of employees to create')
        parser.add_argument('--days', type=int, default=30, help='Number of past days to create attendance for')

    def handle(self, *args, **options):
        num_employees = options['employees']
        num_days = options['days']

        # 1) Departments
        dept_names = ['Engineering', 'HR', 'Sales', 'Marketing', 'Finance', 'Operations']
        departments = []
        for name in dept_names:
            dept, _ = Department.objects.get_or_create(name=name)
            departments.append(dept)
        self.stdout.write(self.style.SUCCESS(f"Departments ready: {len(departments)}"))

        # 2) Employees
        employees = []
        for _ in range(num_employees):
            first = fake.first_name()
            last = fake.last_name()
            email = f"{first.lower()}.{last.lower()}{random.randint(1,9999)}@example.com"
            emp = Employee.objects.create(
                first_name=first,
                last_name=last,
                email=email,
                phone_number=fake.phone_number(),
                address=fake.address(),
                date_of_joining=fake.date_between(start_date='-2y', end_date='today'),
                department=random.choice(departments),
                is_active=True
            )
            employees.append(emp)
        self.stdout.write(self.style.SUCCESS(f"Employees created: {len(employees)}"))

        # 3) Attendance for last N days
        today = date.today()
        statuses = ['present', 'present', 'present', 'late', 'absent']  # more present than absent
        total_att = 0
        for emp in employees:
            for i in range(num_days):
                d = today - timedelta(days=i)
                # Skip weekends optional:
                if d.weekday() >= 5:
                    continue
                Attendance.objects.get_or_create(
                    employee=emp, date=d,
                    defaults={'status': random.choice(statuses)}
                )
                total_att += 1
        self.stdout.write(self.style.SUCCESS(f"Attendance records created: ~{total_att}"))

        # 4) Performance (1–5 rating, monthly-ish)
        total_perf = 0
        for emp in employees:
            for i in range(6):  # last 6 months
                review_date = today - timedelta(days=30*i + random.randint(0, 10))
                Performance.objects.create(
                    employee=emp,
                    rating=random.randint(1,5),
                    review_date=review_date,
                    remarks=fake.sentence()
                )
                total_perf += 1
        self.stdout.write(self.style.SUCCESS(f"Performance reviews created: {total_perf}"))

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
