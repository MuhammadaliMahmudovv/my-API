from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, Profile
from .serializers import CustomUserSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ProtectedHello(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, authenticated user!"})


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


# --


@api_view(["GET"])
def ProfileList(request):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def ProfileDetailView(request, pk):
    profile = Profile.objects.get(pk=pk)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def ProfileCreate(request):
    serializer = ProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

    
@api_view(["POST"])
def ProfileUpdate(request, pk):
    profile = Profile.objects.get(pk=pk)
    serializer = ProfileSerializer(instance=profile, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
def profileDelete(request, pk):
    profile = Profile.objects.get(pk=pk).delete()

    return Response("profile succsesfully deleted!")
