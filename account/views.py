from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny

from account.serializers import UserSerializer
from project.permissions import IsOwnAccount

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('=username', '=email', '=phone',
                     'first_name', 'last_name')

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (AllowAny,)

        else:
            self.permission_classes = (IsOwnAccount,)
        return super().get_permissions()

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
