from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import StudentRecord
from core.serializers import StudentRecordSerializer
from core.permissions import IsAdminGroup, IsAdminOrFacultyGroup
import logging
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse

logger = logging.getLogger('django')

class StudentRecordViewSet(ModelViewSet):
    serializer_class = StudentRecordSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return StudentRecord.objects.all()
        return StudentRecord.objects.filter(owner=user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminGroup]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsAdminOrFacultyGroup]
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        owner_id = self.request.data.get('owner')
        
        if owner_id:
            serializer.save(owner_id=owner_id)
        else:
            serializer.save(owner=self.request.user)

@ratelimit(key='ip', rate='5/m', block=True)
def secure_login_test(request):
    logger.warning("Multiple failed login attempts detected from IP: %s", request.META.get('REMOTE_ADDR'))
    return JsonResponse({"message": "Login attempt processed securely."})
