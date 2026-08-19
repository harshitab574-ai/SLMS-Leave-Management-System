from django.db import models
from django.contrib.auth.models import User

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    address = models.TextField()
    joining_date = models.DateField()

    image = models.ImageField(
        upload_to='staff/',
        blank=True,
        null=True
    )

    # Leave Balance
    casual_leave = models.PositiveIntegerField(default=12)
    sick_leave = models.PositiveIntegerField(default=10)
    earned_leave = models.PositiveIntegerField(default=15)

    def __str__(self):
        return self.name


class Leave(models.Model):
    LEAVE_TYPE = [
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Earned', 'Earned'),
    ]

    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE)
    reason = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.staff.name} - {self.leave_type}"