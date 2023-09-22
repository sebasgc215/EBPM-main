from django.shortcuts import render
from microservice.models import DiagramText
from microservice.serialiazers import DiagramTextSerialiazer
from core.crud.standard import Crud
from rest_framework.decorators import api_view


crudObject = Crud(DiagramTextSerialiazer, DiagramText)
# Create your views here.
@api_view(["POST"])
def create(request):
    diagram_create = crudObject.create(request)
    return diagram_create

@api_view(['GET'])
def list(request, projectId):
    diagramList = crudObject.list(request, "project", projectId)
    return diagramList

@api_view(['GET'])
def get(request, diagramId):
    diagramGet = crudObject.get(request, diagramId)
    return diagramGet

@api_view(['DELETE'])
def delete(request, diagramId):
    diagramDelete = crudObject.delete(
        diagramId, 'The diagram has been successfully removed')
    return diagramDelete