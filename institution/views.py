from django.db.models import query
from django.shortcuts import render,get_object_or_404
from .models import TheClass
from .serializers import TheClassModelSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

 
@api_view(["GET"])
def getapi(request,pk):
    if request.method == "GET":
        query = TheClass.objects.filter(id=pk)
        serializer= TheClassModelSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

