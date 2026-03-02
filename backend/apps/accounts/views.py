from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.common.responses import success_response
from .serializers import RegisterSerializer, UserSerializer
from .services import create_user

def set_auth_cookies(response, refresh, access):
    cookie_max_age = 3600 * 24 * 7 # 7 days
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        max_age=cookie_max_age,
        secure=not settings.DEBUG,
        httponly=True,
        samesite='Lax'
    )
    response.set_cookie(
        key='access_token',
        value=str(access),
        max_age=3600, # 1 hour
        secure=not settings.DEBUG,
        httponly=True,
        samesite='Lax'
    )

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            set_auth_cookies(response, refresh_token, access_token)
            # Remove tokens from JSON response for security against XSS
            del response.data['access']
            del response.data['refresh']
            response.data['message'] = "Login successful"
        return response

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return success_response(message="No refresh token cookie found", status_code=status.HTTP_401_UNAUTHORIZED)
        
        # Inject the refresh token into data to trick DRF Simple JWT
        request.data['refresh'] = refresh_token
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                access_token = response.data.get('access')
                refresh_token_resp = response.data.get('refresh', refresh_token)
                set_auth_cookies(response, refresh_token_resp, access_token)
                if 'access' in response.data:
                    del response.data['access']
                if 'refresh' in response.data:
                    del response.data['refresh']
                response.data['message'] = "Token refreshed"
            return response
        except TokenError as e:
            return success_response(message=e.args[0], status_code=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'register'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = create_user(**serializer.validated_data)
        refresh = RefreshToken.for_user(user)
        
        data = {
            'user': UserSerializer(user).data
        }
        res = success_response(data, "User created successfully", status.HTTP_201_CREATED)
        set_auth_cookies(res, refresh, refresh.access_token)
        return res

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            # Blacklist removed to maintain compatibility without token_blacklist app
            res = success_response(message="Logged out successfully")
            res.delete_cookie('access_token')
            res.delete_cookie('refresh_token')
            return res
        except Exception:
            res = success_response(message="Logged out successfully (invalid token)")
            res.delete_cookie('access_token')
            res.delete_cookie('refresh_token')
            return res

class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response(serializer.data, "User fetched successfully")
