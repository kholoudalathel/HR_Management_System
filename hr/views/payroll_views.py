from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from hr.models.payroll_models import Payroll
from hr.serializers.payroll_serializers import PayrollSerializer
from hr.utils import is_in_group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Admin only - create payroll

@swagger_auto_schema(
    method='post',
    request_body=PayrollSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={201: PayrollSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payroll_create(request):
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    data['net_salary'] = float(data['basic_salary']) + float(data['allowances']) - float(data['deductions'])

    serializer = PayrollSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin only - update payroll
@swagger_auto_schema(
    method='put',
    request_body=PayrollSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={200: PayrollSerializer()}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def payroll_update(request, pk):
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        payroll = Payroll.objects.get(pk=pk, is_active=True)
    except Payroll.DoesNotExist:
        return Response({"error": "Payroll not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data['net_salary'] = float(data['basic_salary']) + float(data['allowances']) - float(data['deductions'])

    serializer = PayrollSerializer(payroll, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#a list payroll admin sees all, users see their own
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payroll_list(request):
    if is_in_group(request.user, 'admin_users'):
        payrolls = Payroll.objects.filter(is_active=True)
    elif is_in_group(request.user, 'limited_users') or is_in_group(request.user, 'restricted_users'):
        payrolls = Payroll.objects.filter(user=request.user, is_active=True)
    else:
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    serializer = PayrollSerializer(payrolls, many=True)
    return Response(serializer.data)

# Retrieve Payroll (Users see their own, admins see all)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payroll_detail(request, pk):
    try:
        payroll = Payroll.objects.get(pk=pk, is_active=True)
        if payroll.user != request.user and not is_in_group(request.user, 'admin_users'):
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    except Payroll.DoesNotExist:
        return Response({"error": "Payroll not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PayrollSerializer(payroll)
    return Response(serializer.data)

# soft delete payroll (admin only)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def payroll_delete(request, pk):
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        payroll = Payroll.objects.get(pk=pk, is_active=True)
    except Payroll.DoesNotExist:
        return Response({"error": "Payroll not found"}, status=status.HTTP_404_NOT_FOUND)

    payroll.is_active = False
    payroll.save()
    return Response({"message": "Payroll record soft-deleted successfully"}, status=status.HTTP_204_NO_CONTENT)