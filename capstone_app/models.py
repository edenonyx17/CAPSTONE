from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Task(models.Model):
  # Labels and category
  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
  ]
  PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
  ]
  CATEGORY_CHOICES = [
    ('work', 'Work'),
    ('personal', 'Personal'),
    ('shopping', 'Shopping'),
    ('other', 'Other'),
  ]

  # Task fields
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True, null=True)
  due_date = models.DateField(blank=True, null=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
  category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
  date_created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

  # Reminder
  def is_overdue(self):
    return self.due_date and self.due_date < date.today() and self.status == 'pending'




