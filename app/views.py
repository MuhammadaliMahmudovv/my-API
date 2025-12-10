from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer


@api_view(["GET"])
def CustomUserList(request):
    user = CustomUser.objects.filter(is_staff=False).order_by("-created_at")
    serializer = CustomUserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def CustomUserDetailView(request, pk):
    user = CustomUser.objects.filter(is_staff=False).get(pk=pk)
    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def CustomUserCreate(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def CustomUserUpdate(request, pk):
    user = CustomUser.objects.get(pk=pk)
    serializer = CustomUserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
def CustomUserDelete(request, pk):
    user = CustomUser.objects.get(pk=pk).delete()

    return Response("user succsesfully deleted!")
