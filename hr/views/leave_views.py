from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from hr.models.leave_models import Leave
from hr.serializers.leave_serializers import LeaveSerializer
from hr.utils import is_in_group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@api_view(['GET'])
@permission_classes([AllowAny])  # No authentication required
def health_check(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


# create a new leave (authenticated users only)
@swagger_auto_schema(
    method='post',
    request_body=LeaveSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={201: LeaveSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_create(request):
    if is_in_group(request.user, 'admin_users') or is_in_group(request.user, 'limited_users') or is_in_group(
            request.user, 'restricted_users'):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

# update a Leave (admin can update anyone's but each user can update their own)
@swagger_auto_schema(
    method='put',
    request_body=LeaveSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token <your_token>",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={200: LeaveSerializer()}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def leave_update(request, pk):
    try:
        leave = Leave.objects.get(pk=pk, is_active=True)

        # Only allow the user to update their own leave or admins to update any
        if leave.user != request.user and not is_in_group(request.user, 'admin_users'):
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

    except Leave.DoesNotExist:
        return Response({"error": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LeaveSerializer(leave, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# list leaves admin sees all user sees their own
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_list(request):
    if is_in_group(request.user, 'admin_users'):
        leaves = Leave.objects.filter(is_active=True)
    elif is_in_group(request.user, 'limited_users'):
        leaves = Leave.objects.filter(user=request.user, is_active=True)
    else:
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    serializer = LeaveSerializer(leaves, many=True)
    return Response(serializer.data)

# get a single Leave
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_detail(request, pk):
    try:
        leave = Leave.objects.get(pk=pk, is_active=True)
        if leave.user != request.user and not is_in_group(request.user, 'admin_users'):
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    except Leave.DoesNotExist:
        return Response({"error": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LeaveSerializer(leave)
    return Response(serializer.data)


#users can delete their own admins can delete anyone's leave instance
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_delete(request, pk):
    try:
        leave = Leave.objects.get(pk=pk, is_active=True)
        if leave.user != request.user and not is_in_group(request.user, 'admin_users'):
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    except Leave.DoesNotExist:
        return Response({"error": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

    leave.is_active = False
    leave.save()
    return Response({"message": "Leave deleted successfully"}, status=status.HTTP_204_NO_CONTENT)