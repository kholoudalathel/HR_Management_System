
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from hr.models.employee_models import Employee
from hr.serializers.employee_serializers import EmployeeSerializer
from hr.utils import is_in_group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@api_view(['GET'])
@permission_classes([AllowAny])  # No authentication required
def health_check(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


# Create a new employee (admin only)

@swagger_auto_schema(
    method='post',
    request_body=EmployeeSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={201: EmployeeSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employee_create(request):
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update an existing employee (admin only)
@swagger_auto_schema(
    method='put',
    request_body=EmployeeSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={200: EmployeeSerializer()}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def employee_update(request, pk):
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        employee = Employee.objects.get(pk=pk, is_active=True)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# list all employees admin sees all, users their own profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list(request):
    if is_in_group(request.user, 'admin_users'):
        employees = Employee.objects.filter(is_active=True)
    elif is_in_group(request.user, 'limited_users'):
        employees = Employee.objects.filter(email=request.user.email, is_active=True)
    else:
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

# get a single employee users can only see their own, admins can see all
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk, is_active=True)
        if not is_in_group(request.user, 'admin_users') and employee.email != request.user.email:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)


# admin deletes an employee
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def employee_delete(request, pk):
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        employee = Employee.objects.get(pk=pk, is_active=True)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    employee.is_active = False
    employee.save()
    return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)