from django.db.models import Count, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from ads.models import User
from ads.serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by('username').annotate(total_ads=Count(
            expression='ad',
            filter=Q(ad__is_published=True)
        ))
        return super().get(request, *args, **kwargs)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
