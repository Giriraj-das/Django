import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.permissions import AdUpdateDeletePermission
from ads.serializers import AdListSerializer, AdDetailSerializer, AdUpdateSerializer, AdDestroySerializer
from ads.models import Ad, User, Category


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.select_related('author', 'category').order_by('price')

        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data["name"],
            author=get_object_or_404(User, pk=ad_data["author_id"]),
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category=get_object_or_404(Category, pk=ad_data["category_id"]),
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.first_name + " " + ad.author.last_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        })


# @method_decorator(csrf_exempt, name="dispatch")
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = ["name", "author", "price", "description", "is_published", "category"]
#
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         ad_data = json.loads(request.body)
#         if "name" in ad_data:
#             self.object.name = ad_data["name"]
#         if "author" in ad_data:
#             self.object.author = get_object_or_404(User, pk=ad_data["author_id"])
#         if "price" in ad_data:
#             self.object.price = ad_data["price"]
#         if "description" in ad_data:
#             self.object.description = ad_data["description"]
#         if "is_published" in ad_data:
#             self.object.is_published = ad_data["is_published"]
#         if "category" in ad_data:
#             self.object.category = get_object_or_404(Category, pk=ad_data["category_id"])
#         self.object.save()
#
#         return JsonResponse({
#             "id": self.object.id,
#             "name": self.object.name,
#             "author_id": self.object.author_id,
#             "author": self.object.author.username,
#             "price": self.object.price,
#             "description": self.object.description,
#             "is_published": self.object.is_published,
#             "category_id": self.object.category_id,
#             "image": self.object.image.url if self.object.image else None,
#         })

class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [AdUpdateDeletePermission]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [AdUpdateDeletePermission]


# @method_decorator(csrf_exempt, name="dispatch")
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "deleted"}, status=204)


@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ("image",)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })
