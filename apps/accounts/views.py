from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.common.responses import success_response
from .serializers import RegisterSerializer, UserSerializer
from .services import create_user

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'register'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = create_user(**serializer.validated_data)
        refresh = RefreshToken.for_user(user)
        
        data = {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
        return success_response(data, "User created successfully", status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response(message="Logged out successfully")
        except Exception:
            return success_response(message="Invalid token or already logged out", status_code=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response(serializer.data, "User fetched successfully")
