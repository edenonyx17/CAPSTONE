from django.contrib import admin
from .models import Task

# Register your models here
""""@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'due_date', 'status', 'priority', 'category', 'date_created')
  list_filter = ('status', 'priority', 'category')
  search_fields = ('title', 'description')
  ordering = ('-date_created',)
  date_hierarchy = 'date_created'
  readonly_fields = ('date_created',)

  def save_model(self, request, obj, form, change):
    if not change:
      obj.user = request.user
    super().save_model(request, obj, form, change)
    """

admin.site.register(Task)