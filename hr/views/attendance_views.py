from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from hr.models.attendance_models import Attendance
from hr.serializers.attendance_serializers import AttendanceSerializer
from hr.utils import is_in_group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create attendance (admin and limited users)

@swagger_auto_schema(
    method='post',
    request_body=AttendanceSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={201: AttendanceSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_create(request):
    # Only admin_users and limited_users can create attendance records
    if is_in_group(request.user, 'admin_users') or is_in_group(request.user, 'limited_users'):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user.employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

# Update attendance (admin only)
@swagger_auto_schema(
    method='put',
    request_body=AttendanceSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={200: AttendanceSerializer()}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def attendance_update(request, pk):
    # Only admin_users can update attendance records
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        attendance = Attendance.objects.get(pk=pk, is_active=True)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AttendanceSerializer(attendance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# list Attendance (User sees their own, admin sees all)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_list(request):
    if is_in_group(request.user, 'admin_users'):
        attendances = Attendance.objects.filter(is_active=True)
    elif is_in_group(request.user, 'limited_users'):
        attendances = Attendance.objects.filter(employee=request.user.employee, is_active=True)
    else:
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)

#get a single attendance record admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_detail(request, pk):
    try:
        attendance = Attendance.objects.get(pk=pk, is_active=True)
        if attendance.employee != request.user.employee and not is_in_group(request.user, 'admin_users'):
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AttendanceSerializer(attendance)
    return Response(serializer.data)


#soft delete attendance (admin only)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def attendance_delete(request, pk):
    if not is_in_group(request.user, 'admin_users'):
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    try:
        attendance = Attendance.objects.get(pk=pk, is_active=True)
        attendance.is_active = False
        attendance.save()
        return Response({"message": "Attendance record soft-deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)