from django.db import models
from django.contrib.auth.models import User

class Leave(models.Model):
    LEAVE_TYPES = (
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation Leave'),
        ('casual', 'Casual Leave'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type}"