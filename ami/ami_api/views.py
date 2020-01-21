from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from .customutils import *
# Create your views here.
from rest_framework import viewsets, request
import ImageTools.index_generator as ig
from ImageTools.stitchSet import StitchSet as ss
import ImageTools.utils as imutils
from .serializers import *
from .models import *

class GeoNoteViewSet(viewsets.ModelViewSet):
    queryset = GeoNote.objects.all().order_by('user')
    serializer_class = GeoNoteSerializer
    @action(methods=['get'], detail=True)
    def get_notes(self, httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            print('req data:',req_data)
            conditions=' AND'.join([" {}='{}'".format(key,value) for key, value in req_data.items()])
            print(conditions)
            command='SELECT * FROM ami_api_geonote WHERE'+conditions
            print(command)
            resp=sql_cursor.execute(command)
            resp=resp.fetchall()
            keys = ['id','user','field','value','latitude','date','longitude']
            response = [{key:value for key, value in zip(keys, marker)} for marker in resp]
            print(resp)
            return JsonResponse({'notes':response})
        else:
            return HttpResponse(status=400)
    @action(methods=['get'], detail=True)
    def get_next_id(self, httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            max_id=sql_cursor.execute('SELECT MAX(id) FROM ami_api_geonote')
            max_id=sql_cursor.fetchone()[0]+1
            return JsonResponse({'id':max_id})
    @action(methods=['get'], detail=True)
    def del_id(self, httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            sql_cursor.execute('DELETE from ami_api_geonote WHERE id=?',[req_data['id']])
            sql.commit()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
        
    @action(methods=['get'], detail=True)
    def update_add_note(self, httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            print('req data:',req_data)
            ids=sql_cursor.execute('SELECT id FROM ami_api_geonote')
            ids = [_[0] for _ in ids.fetchall()]
            print(ids)
            print(int(req_data['id']))
            if int(req_data['id']) in ids:
                print('updating')
                sql_cursor.execute('UPDATE ami_api_geonote SET date=?, value=? WHERE id=?',
                [req_data['date'], req_data['value'], req_data['id']])
                sql.commit()
                return HttpResponse(status=200)
            else:
                print('inserting')
                sql_cursor.execute('INSERT INTO ami_api_geonote (id, user, field, date, latitude, longitude, value) VALUES (?,?,?,?,?,?,?)',
                    [req_data['id'],req_data['user'],req_data['field'],req_data['date'],req_data['latitude'],req_data['longitude'],req_data['value']])
                sql.commit()
                return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('user')
    serializer_class = UserSerializer
    @action(methods=['get'], detail=True)
    #TODO: make this not so blatantly insecure
    def authenticate(self, httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            resp = sql_cursor.execute('SELECT * FROM ami_api_user WHERE user=? AND password=?;',
                                        [req_data['user'],req_data['password']])
            sql_init_response = [_ for _ in resp][0]
            print(sql_init_response)
            if not sql_init_response:
                return JsonResponse({'correct':0,'fields':[]})
            else:
                return JsonResponse({'correct':1,'fields':sql_init_response[3].split(',')})
        else:
            return HttpResponse(status=400)
        

class StackedImageViewSet(viewsets.ModelViewSet):
    queryset = StackedImage.objects.all().order_by('user')
    serializer_class = StackedImageSerializer
    @action(methods=['get'], detail=True)
    def request_dates(self,httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            print('req data:',req_data)
            conditions=' AND'.join([" {}='{}'".format(key,value) for key, value in req_data.items()])
            print(conditions)
            command='SELECT date FROM ami_api_stackedimage WHERE'+conditions
            print(command)
            resp=sql_cursor.execute(command)
            resp=[_ for _ in resp][0]
            print(resp)
            return JsonResponse({'dates':resp})
            
        else:
            return HttpResponse(status=400)

class OverlayImageViewSet(viewsets.ModelViewSet):
    queryset = OverlayImage.objects.all().order_by('user')
    serializer_class = OverlayImageSerializer
    @action(methods=['get'], detail=True)
    def request_overlay(self,httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            print(req_data)
            resp = sql_cursor.execute('SELECT * FROM ami_api_overlayimage WHERE user=? AND field=? AND date=? AND index_name=?;',
                                        [req_data['user'],req_data['field'],req_data['date'],req_data['index_name']])
            sql_init_response = [_ for _ in resp]
            print(sql_init_response)
            if not sql_init_response:
                #this means that there is not an overlay that meets the qualifications
                resp2=sql_cursor.execute('SELECT filepath, demfilepath FROM ami_api_stackedimage WHERE user=? AND field=? AND date=?;', 
                                        [req_data['user'],req_data['field'],req_data['date']])
                sql_sec_response = [_ for _ in resp2]
                print(sql_sec_response)
                if sql_sec_response:
                    #if there is a stacked image that can be used, generate the requested index from that
                    imagefilepath = sql_sec_response[0][0]
                    demfilepath = sql_sec_response[0][1]
                    stitch = ss(imagefilepath,demfilepath, output_directory=OVERLAY_STORAGE,output_base='test') #TODO: fix output_base
                    stitch.generateIndex(req_data['index_name'])
                    tif, scale = stitch.exportGeneratedIndicesAsColorImages()[0]
                    png=imutils.convert(tif,tif.replace('.tif','.png'))
                    bounds = get_tif_bbox(tif)
                    data = {'available':1,'png':png, 'bounds':bounds,'scale':scale}
                    max_id=sql_cursor.execute('SELECT MAX(id) FROM ami_api_overlayimage')
                    print(max_id)
                    max_id = [_ for _ in max_id][0]
                    print(max_id)
                    
                    max_id=(max_id[0] if max_id[0] else 0)+1
                    print(max_id)
                    sql_cursor.execute('INSERT INTO ami_api_overlayimage (id, user, field, index_name, date, filepath, tiffilepath, scalefilepath) VALUES (?,?,?,?,?,?,?,?);',
                                        [max_id, req_data['user'],req_data['field'], req_data['index_name'],req_data['date'],png, tif, scale])
                    sql.commit()
                    del sql
                else:
                    #there is no available data and the default response will send
                    return HttpResponse(status=404)
            else:
                #read filepaths from sql_init_response
                png=sql_init_response[0][5]
                bounds = get_tif_bbox(sql_init_response[0][7])
                scale=sql_init_response[0][6]
                data = {'available':1,'png':png, 'bounds':bounds,'scale':scale}
        else:
            return HttpResponse(status=400)
        return JsonResponse(data)
    @action(methods=['get'], detail=True)
    def possible_overlays(self,httprequest: HttpRequest, pk=None):
        if httprequest.method == 'GET':
            overlays = [key for key in ig.colormaps.keys()]
            return JsonResponse({'overlays':overlays})
        else:
            return HttpResponse(status=400)


