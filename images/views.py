from rest_framework import authentication, permissions, status
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from images.models import Image
from users.models import User
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from images.serializers import ImageSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
import uuid
from PIL import Image as Imaage
import _io
from _io import BytesIO 
from django.conf import settings

# Create your views here
class ImagePost(APIView):
    permission_classes = (permissions.AllowAny, )
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file_list = request.FILES.getlist('image')
        if 'image' not in request.data or len(file_list) == 0:
            raise ParseError('Empty file contnet!')
        file_uris = []
        for file in file_list:
            file_name = f'{str(uuid.uuid4().hex)}.png'

            img = Imaage.open(file)
            output = _io.BytesIO()

            img.save(output, format='PNG')
            output.seek(0)

            img = Image()
            img.title = file_name
            img.user = None
            img.image.save(file_name, output)
            img.description = ''
            img.save()
            file_uris.append(f'{settings.SERVER_URL}/{settings.SERVER_STATIC_FILES}/{img.image.name}')
        return Response(file_uris, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        return Response(request.data)

