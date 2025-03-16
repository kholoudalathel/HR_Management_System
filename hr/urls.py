from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.employee_views import (
    health_check,
    employee_create,
    employee_list,
    employee_detail,
    employee_update,
    employee_delete,
)
from hr.views.attendance_views import  (attendance_create,attendance_list,attendance_update,attendance_delete,attendance_detail)
from hr.views.leave_views import (health_check,leave_create,leave_list,leave_detail,leave_update,leave_delete)
from hr.views.payroll_views import (payroll_create,payroll_list,payroll_detail,payroll_update,payroll_delete)




urlpatterns = [
    path('employees/health/', health_check, name='employees-health-check'),
    path('employees/', employee_list, name='employee-list'),
    path('employees/create/', employee_create, name='employee-create'),
    path('employees/<int:pk>/', employee_detail, name='employee-detail'),
    path('employees/<int:pk>/update/', employee_update, name='employee-update'),
    path('employees/<int:pk>/delete/', employee_delete, name='employee-delete'),
    path('leaves/health/', health_check, name='leaves-health-check'),
    path('leaves/', leave_list, name='leave-list'),
    path('leaves/create/', leave_create, name='leave-create'),
    path('leaves/<int:pk>/', leave_detail, name='leave-detail'),
    path('leaves/<int:pk>/update/', leave_update, name='leave-update'),
    path('leaves/<int:pk>/delete/', leave_delete, name='leave-delete'),
    path('payrolls/', payroll_list, name='payroll-list'),
    path('payrolls/create/', payroll_create, name='payroll-create'),
    path('payrolls/<int:pk>/', payroll_detail, name='payroll-detail'),
    path('payrolls/<int:pk>/update/', payroll_update, name='payroll-update'),
    path('payrolls/<int:pk>/delete/', payroll_delete, name='payroll-delete'),
    path('attendances/', attendance_list, name='attendance-list'),
    path('attendances/<int:pk>/', attendance_detail, name='attendance-detail'),
    path('attendances/create/', attendance_create, name='attendance-create'),
    path('attendances/<int:pk>/update/', attendance_update, name='attendance-update'),
    path('attendances/<int:pk>/delete/', attendance_delete, name='attendance-delete'),
]