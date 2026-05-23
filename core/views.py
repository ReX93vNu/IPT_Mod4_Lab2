import logging

from django.http import JsonResponse
from django.contrib.auth import authenticate  

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django_ratelimit.decorators import ratelimit
from cryptography.fernet import InvalidToken

from core.models import StudentRecord, cipher  
from core.serializers import StudentRecordSerializer
from core.permissions import IsAdminGroup, IsAdminOrFacultyGroup

logger = logging.getLogger('core')

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


# login api for username and pass with bruteforce protection. Just realized this might be redundant since i merged this with mod4_lab1 
@ratelimit(key='ip', rate='5/m', block=True) 
@api_view(['POST'])
@permission_classes([AllowAny]) 
def login_view(request):
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        return JsonResponse({"message": "Login successful! Proceed to payment endpoint."})
    else:
        logger.warning("Multiple failed login attempts detected from IP: %s", request.META.get('REMOTE_ADDR'))
        return JsonResponse({"error": "Invalid credentials. Unauthorized."}, status=401)


# payment api with encrypted payload and decryption and bruteforce protection. i cant figure out how to apply the encrypted payload decryption part with the provided ratelimit code, so seperated them instead.
@ratelimit(key='ip', rate='5/m', block=True) 
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # cant add a custom log message because authentication is handled by django. i cant figure out how to make it work while also satsifying the requirements
def secure_payment_api(request):
    
    encrypted_data = request.data.get('secret_data', '')
    
    try:
        cipher.decrypt(encrypted_data.encode('utf-8'))
        return JsonResponse({"message": "Secure payment processed successfully."})
        
    except InvalidToken:
        logger.warning("SECURITY ALERT: Invalid encrypted payload spam detected")
        return JsonResponse({"error": "Invalid encrypted payload detected."}, status=400)
    except Exception:
        return JsonResponse({"error": "Malformed request."}, status=400)
