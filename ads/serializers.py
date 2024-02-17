from rest_framework import serializers

from ads.models import Location, User, Ad


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    category_name = serializers.CharField(read_only=True)

    class Meta:
        model = Ad
        exclude = ('author', 'category')


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
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

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
        if "locations" in self.initial_data:
            self._locations = self.initial_data.pop("locations")
        else:
            self._locations = []
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
