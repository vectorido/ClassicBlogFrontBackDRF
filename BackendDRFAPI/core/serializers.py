from django.contrib.auth.models import User
from rest_framework import serializers
from taggit.models import Tag
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from .models import Post, Comment


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ("id", "h1", "title", "slug", "description", "content", "image", "created_at", "author",
                  "tags")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'post', 'username', 'text', 'created_date')

# class CommentSerializer(serializers.ModelSerializer):
#     username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
#     post = serializers.SlugRelatedField(slug_field="slug", queryset=Post.objects.all())
#
#     class Meta:
#         model = Comment
#         fields = ("id", "post", "username", "text", "created_date")
#         lookup_field = 'id'
#         extra_kwargs = {
#             'url': {'lookup_field': 'id'}
#         }
# Сериализаторы позволяют преобразовывать сложные данные, такие как наборы запросов и экземпляры моделей, в
# собственные типы данных Python, которые затем могут быть легко преобразованы в JSON , XML или другие типы
# содержимого


# Сериализаторы в REST framework работают аналогично классам Django Form и ModelForm
# Создание сериализатора очень похоже на создание формы на основе модели.
