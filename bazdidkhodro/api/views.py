from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import generics
from bazdidkhodro.models import *
from bazdidkhodro.api.serializers import (
    InsurerShowSerializer,
    InsurerCreateSerializer,
    VisitCreateSerializer,
    DocumentCreateSerializer,
    DocumentFileCreateSerializer,
    ImageCreateSerializer,
    VisitShowSerializer,
)
from account.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
from django.http.request import QueryDict
import traceback


class InsurerListAPIView(generics.ListAPIView):
    serializer_class = InsurerShowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='visitor').exists() or self.request.user.groups.filter(name='employee').exists():
            return Insurer.objects.all()
        return Insurer.objects.none()


class InsurerCreateAPIView(generics.CreateAPIView):
    serializer_class = InsurerCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        if self.request.user.groups.filter(name='visitor').exists() or self.request.user.groups.filter(name='employee').exists():
            request.data["created_by"] = request.user.id
            request.data["pelak"] = request.data["p1"] + "-" + request.data["p2"] + "-" + request.data["p3"] + "-" + request.data["p4"]
            insurer_serializer = InsurerCreateSerializer(data=request.data)
            if insurer_serializer.is_valid():
                insurer_serializer.save()
                return Response(status=status.HTTP_200_OK, data={'state': '1','message':'insurer save done'})
            else:
                if Insurer.objects.filter(mobile=request.data["mobile"]).count()==1:
                    return Response(status=status.HTTP_200_OK, data={'state': '-1', 'message': 'mobile in used'})
                if Insurer.objects.filter(pelak=request.data["pelak"]).count()==1:
                    return Response(status=status.HTTP_200_OK, data={'state': '-2', 'message': 'pelak in used'})
        else:
            return Response(status=status.HTTP_200_OK, data={'state': '0','message':'you ara not visitor'})
        return Response(status=status.HTTP_200_OK, data={'state': '0','message':'bad request'})


class VisitCreateAPIView(generics.CreateAPIView):
    serializer_class = VisitCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='visitor').exists():
            request.data['visitor'] = request.user.id
            cur_obj = Visit.objects.filter(insurer=request.data['insurer'], year=request.data['year'])
            if len(list(cur_obj))==1:
                if list(cur_obj)[0].finished == False and list(cur_obj)[0].visitor.id == request.user.id:
                    images = dict((request.data).lists()).get('imgs')
                    visit_id = list(cur_obj)[0].id
                    for imgByte in images:
                        image_data = {'visit': visit_id, 'img': imgByte}
                        image_serializer = ImageCreateSerializer(data=image_data)
                        if image_serializer.is_valid():
                            image_serializer.save()
                            img_name = image_serializer.data.get('img')[1:]
                            img = Image.open(img_name)
                            w = img.__dict__.get('_size')[0]
                            h = img.__dict__.get('_size')[1]
                            if w > 1000:
                                w = w - int(w / 7)
                            else:
                                w = w - 130
                            if h > 1000:
                                h = h - int(h / 20)
                            else:
                                h = h - 25
                            draw = ImageDraw.Draw(img)
                            font_size = 15
                            if int(w / 1000) > 0:
                                font_size = int(int(int(2 - int(int(w / 1000) * 0.19)) * w) / 100)
                            font = ImageFont.truetype(font="fonts/arial.ttf", size=font_size)
                            # draw.text((x, y),"Sample Text",(r,g,b))
                            draw.text((w, h), str(datetime.now().day) + "/" + str(datetime.now().month) + "/" + str(
                                datetime.now().year) + "  " + str(datetime.now().hour) + ":" + str(
                                datetime.now().minute), (255, 255, 255), font=font)
                            img.save(img_name)
                    return Response(status=status.HTTP_200_OK, data={'state': '1', 'message': 'visit append done '})
                else:
                    return Response(status=status.HTTP_200_OK, data={'state': '-1', 'message': 'visit finished or you dont permission'})
            else:
                request.data['visitor'] = request.user.id
                images = dict((request.data).lists()).get('imgs')
                visit_serializer = VisitCreateSerializer(data = request.data)
                if visit_serializer.is_valid():
                    visit_serializer.save()
                    visit_id = visit_serializer.data.get("id")
                    for imgByte in images:
                        image_data = {'visit':visit_id,'img':imgByte}
                        image_serializer = ImageCreateSerializer(data=image_data)
                        if image_serializer.is_valid():
                            image_serializer.save()
                            img_name = image_serializer.data.get('img')[1:]
                            img = Image.open(img_name)
                            w = img.__dict__.get('_size')[0]
                            h = img.__dict__.get('_size')[1]
                            if w > 1000:
                                w = w - int( w / 7 )
                            else:
                                w = w - 130
                            if h > 1000 :
                                h = h - int( h / 20 )
                            else:
                                h = h - 25
                            draw = ImageDraw.Draw(img)
                            font_size = 15
                            if int(w/1000) > 0:
                                font_size = int(int(int( 2 - int(int( w / 1000 ) * 0.19) ) * w) / 100)
                            font = ImageFont.truetype(font="fonts/arial.ttf",size= font_size)
                            # draw.text((x, y),"Sample Text",(r,g,b))
                            draw.text((w, h), str(datetime.now().day)+"/"+str(datetime.now().month)+"/"+str(datetime.now().year)+"  "+str(datetime.now().hour)+":"+str(datetime.now().minute), (255, 255, 255),font=font)
                            img.save(img_name)
                    return Response(status=status.HTTP_200_OK,data={'state':'1','message':'visit created '})
            return Response(status=status.HTTP_200_OK, data={'state':'0','message': 'send incorret data'})
        else:
            return Response(status=status.HTTP_200_OK,data={'state':'0','message': 'you dont have permission...'})



class DocumentCreateAPIView(generics.CreateAPIView):
    serializer_class = DocumentCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='employee').exists():
            request.data['employee'] = request.user.id
            images = dict((request.data).lists()).get('imgs')
            document_serializer = DocumentCreateSerializer(data = request.data)
            if document_serializer.is_valid():
                document_serializer.save()
                document_id = document_serializer.data.get("id")
                for imgByte in images:
                    document_file_data = {'document':document_id,'file':imgByte}
                    document_file_serializer = DocumentFileCreateSerializer(data=document_file_data)
                    if document_file_serializer.is_valid():
                        document_file_serializer.save()
                return Response(status=status.HTTP_200_OK, data={'state': '1', 'message': 'document created '})
        else:
            return Response(status=status.HTTP_200_OK,data={'state':'0','message': 'you dont have permission...'})



class VisitListAPIView(generics.ListAPIView):
    serializer_class = VisitShowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='visitor').exists():
            return Visit.objects.filter(visitor=self.request.user.id)
        return Visit.objects.none()