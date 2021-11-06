from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import *

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, DjangoMultiPartParser


class RawFileViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    queryset = RawFile.objects.all()
    serializer_class = RawFileSerializer



class ProcessedFileViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    queryset = ProcessedFile.objects.all()
    serializer_class = ProcessedFileSerializer
