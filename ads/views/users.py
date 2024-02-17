import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from ads.models import User, Location
from ads.serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer
from homework import settings


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by('username').annotate(total_ads=Count(
            expression='ad',
            filter=Q(ad__is_published=True)
        ))
        return super().get(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     self.object_list = self.object_list.prefetch_related('locations').order_by('username').annotate(total_ads=Count(
    #         expression='ad',
    #         filter=Q(ad__is_published=True)
    #     ))
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #
    #     users = [{
    #         "id": user.id,
    #         "username": user.username,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "role": user.role,
    #         "age": user.age,
    #         "location": list(map(str, user.locations.all())),
    #         "total_ads": user.total_ads
    #     }
    #         for user in page_obj
    #     ]
    #
    #     response = {
    #         "items": users,
    #         "num_pages": paginator.num_pages,
    #         "total": paginator.count,
    #     }
    #
    #     return JsonResponse(response, safe=False)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    # def get(self, request, *args, **kwargs):
    #
    #     user = self.get_object()
    #     return JsonResponse({
    #         "id": user.id,
    #         "username": user.username,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "role": user.role,
    #         "age": user.age,
    #         "locations": list(map(str, user.locations.all())),
    #     })


# @method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # model = User
    # fields = ["username", "first_name", "last_name", "role", "age", "locations"]

    # def post(self, request, *args, **kwargs):
    #     user_data = json.loads(request.body)
    #
    #     user = User.objects.create(
    #         username=user_data["username"],
    #         password=user_data["password"],
    #         first_name=user_data["first_name"],
    #         last_name=user_data["last_name"],
    #         role=user_data["role"],
    #         age=user_data["age"],
    #     )
    #
    #     for location in user_data["locations"]:
    #         location_obj, _ = Location.objects.get_or_create(name=location)
    #         user.locations.add(location_obj)
    #     user.save()
    #
    #     return JsonResponse({
    #         "id": user.id,
    #         "username": user.username,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "role": user.role,
    #         "age": user.age,
    #         "locations": list(map(str, user.locations.all()))
    #     })


# @method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    # model = User
    # fields = ["username", "password", "first_name", "last_name", "age", "locations"]

    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #     user_data = json.loads(request.body)
    #
    #     if "username" in user_data:
    #         self.object.username = user_data["username"]
    #     if "password" in user_data:
    #         self.object.password = user_data["password"]
    #     if "first_name" in user_data:
    #         self.object.first_name = user_data["first_name"]
    #     if "last_name" in user_data:
    #         self.object.last_name = user_data["last_name"]
    #     if "age" in user_data:
    #         self.object.age = user_data["age"]
    #     if user_data.get("locations", []):
    #         self.object.locations.clear()
    #         for location in user_data["locations"]:
    #             location_obj, _ = Location.objects.get_or_create(name=location)
    #             self.object.locations.add(location_obj)
    #
    #     self.object.save()
    #
    #     return JsonResponse({
    #         "id": self.object.id,
    #         "username": self.object.username,
    #         "first_name": self.object.first_name,
    #         "last_name": self.object.last_name,
    #         "age": self.object.age,
    #         "locations": list(map(str, self.object.locations.all()))
    #     })


# @method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
    # model = User
    # success_url = "/"

    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({"status": "deleted"}, status=204)
