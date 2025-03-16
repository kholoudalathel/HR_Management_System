
from django.contrib import admin
from .models.employee_models import Employee
from .models.attendance_models import Attendance
from .models.leave_models import Leave
from .models.payroll_models import Payroll


from django.contrib import admin

admin.site.site_header = "HR Management Admin Panel"
admin.site.site_title = "HR Admin"
admin.site.index_title = "Welcome to HR Management Dashboard"

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'year', 'net_salary')
    list_filter = ('month', 'year')
    search_fields = ('user__username', 'month')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'position', 'is_active')
    list_display_links = ('first_name', 'last_name')  # Fields that link to the detail view
    list_editable = ('is_active',)  # Editable fields directly from the list view

admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Payroll)
