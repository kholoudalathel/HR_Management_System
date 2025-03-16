from rest_framework import serializers
from hr.models.payroll_models import Payroll

class PayrollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payroll
        fields = '__all__'
        read_only_fields = ['net_salary', 'user']