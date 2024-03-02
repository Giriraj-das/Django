from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ads.models import Location, User, Ad, Selection


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('id', 'name', 'price')


class AdDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    category_name = serializers.CharField(read_only=True)

    class Meta:
        model = Ad
        exclude = ('author', 'category')


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('id',)


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'total_ads')


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ('password',)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ('role',)

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        if self._locations:
            user.locations.clear()

            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                user.locations.add(location_obj)
            user.save()

        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ('id', 'name')


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = ItemsSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ('id',)
