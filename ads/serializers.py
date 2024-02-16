from rest_framework import serializers

from ads.models import Location, User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'role', 'age', 'locations']


# class UserCreateSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required=False)
#     location = serializers.SlugRelatedField(
#         required=False,
#         queryset=Location.objects.first(),
#         slug_field='name'
#     )
#
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def is_valid(self, raise_exception=False):
#         self._locations = self.initial_data.pop("locations")
#         return super().is_valid(raise_exception=raise_exception)
#
#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#
#         for location in self._locations:
#             location_obj, _ = Location.objects.get_or_create(name=location)
#             user.locations.add(location_obj)
#         user.save()
#
#         return user
