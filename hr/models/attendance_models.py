from django.db import models
from .employee_models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField()
    check_out = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"Attendance for {self.employee} on {self.date}"
