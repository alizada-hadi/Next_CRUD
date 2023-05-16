from django.shortcuts import render
from .serializers import BlogSerializer
from rest_framework.views import APIView
from .models import Blog
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            obj = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = Blog.objects.all()
            serializer = BlogSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = Blog.objects.get(pk=pk)
        serializer = BlogSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = Blog.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
