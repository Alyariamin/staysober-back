from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data  # No need for this line, we'll use request.user
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Keep the user logged in
        update_session_auth_hash(request, user)
        
        return Response({"status": "success", "message": "Password updated successfully"})