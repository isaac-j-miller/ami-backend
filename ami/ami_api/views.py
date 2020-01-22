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
            
            max_id=sql_cursor.fetchone()[0]
            if max_id is not None:
                return JsonResponse({'id':max_id+1})
            else:
                return JsonResponse({'id':0})
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
            resp = sql_cursor.execute('SELECT id,user,password,fields FROM ami_api_user WHERE user=? AND password=?;',
                                        [req_data['user'],req_data['password']])
            try:
                sql_init_response = resp.fetchone()
                print(sql_init_response)
                fields = sql_init_response[3].split(',')
                print('fields:',fields)
                if len(fields)==1 and fields[0]=='':
                    origins = {}
                else:
                    origins = {f:self.get_field_location(req_data['user'], f) for f in fields}
                print('origins:',origins)
                return JsonResponse({'correct':1,'fields':fields, 'origins':origins})
            except IndexError:
                return JsonResponse({'correct':0,'fields':[], 'origins': {}})
            except TypeError:
                return JsonResponse({'correct':0,'fields':[], 'origins': {}})
            
        else:
            return HttpResponse(status=400)
    @action(methods=['get'], detail=True)
    def get_next_id(self, httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            max_id=sql_cursor.execute('SELECT MAX(id) FROM ami_api_user')
            max_id=sql_cursor.fetchone()[0]+1
            return JsonResponse({'id':max_id})
        else:
            return HttpResponse(status=400)
    
    @action(methods=['get'], detail=True)
    def add_user(self, httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            sql_cursor.execute('INSERT INTO ami_api_user (id,user,password,fields) VALUES (?,?,?,?)',[req_data['id'],req_data['user'],req_data['password'],''])
            sql.commit()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    def get_field_location(self,user, field):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        resp = sql_cursor.execute('SELECT filepath FROM ami_api_stackedimage WHERE user=? AND field=?',[user, field])
        resp = resp.fetchone()[0]
        with S3GetHandler(resp,IMAGE_STORAGE) as s:
            box = get_tif_bbox(s.tempname)
        lat = (box[1]+box[3])/2
        lon = (box[0]+box[2])/2
        print('field:',field,'response:', resp)
        return {'latitude':lat,'longitude':lon}


class StackedImageViewSet(viewsets.ModelViewSet):
    queryset = StackedImage.objects.all().order_by('user')
    serializer_class = StackedImageSerializer
    @action(methods=['get'], detail=True)
    def request_dates(self,httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()
            #print('req data:',req_data)
            conditions=' AND'.join([" {}='{}'".format(key,value) for key, value in req_data.items()])
            #print(conditions)
            command='SELECT date FROM ami_api_stackedimage WHERE'+conditions
            #print(command)
            resp=sql_cursor.execute(command)
            try:
                resp=[_ for _ in resp][0]
                #print(resp)
                return JsonResponse({'dates':resp})
            except IndexError:
                return JsonResponse({'dates':[]})
            
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
            #print(req_data)
            resp = sql_cursor.execute('SELECT * FROM ami_api_overlayimage WHERE user=? AND field=? AND date=? AND index_name=?;',
                                        [req_data['user'],req_data['field'],req_data['date'],req_data['index_name']])
            sql_init_response = [_ for _ in resp]
            #print(sql_init_response)
            if not sql_init_response:
                #this means that there is not an overlay that meets the qualifications
                resp2=sql_cursor.execute('SELECT filepath, demfilepath FROM ami_api_stackedimage WHERE user=? AND field=? AND date=?;', 
                                        [req_data['user'],req_data['field'],req_data['date']])
                sql_sec_response = [_ for _ in resp2]
                #print(sql_sec_response)
                if sql_sec_response:
                    #if there is a stacked image that can be used, generate the requested index from that
                    imagefilepath = sql_sec_response[0][0]
                    demfilepath = sql_sec_response[0][1]
                    with S3GetHandler(imagefilepath,IMAGE_STORAGE) as img, S3GetHandler(demfilepath,IMAGE_STORAGE) as dem:

                        stitch = ss(img.tempname,
                                    dem.tempname, 
                                    output_directory=IMAGE_STORAGE,
                                    output_base='temp')
                        stitch.generateIndex(req_data['index_name'])
                        tif, scale = stitch.exportGeneratedIndicesAsColorImages()[0]
                        png=imutils.convert(tif,tif.replace('.tif','.png'))
                        bounds = get_tif_bbox(tif)
                        #TODO: clean up this with statement and eliminate redundancy
                        with S3PutHandler(png) as png_s, S3PutHandler(scale) as scale_s, S3PutHandler(tif) as tif_s:
                            png_extra, scale_extra, tif_extra = 0,0,0
                            png_done, scale_done, tif_done = False, False, False
                            while not png_done:
                                png_key=generate_name_base(req_data['user'], req_data['field'], req_data['date'],req_data['index_name'],png_extra,'png')
                                try:
                                    png_s.upload(png_key)
                                    png_key = png_s.get_url()
                                    png_done = True
                                except ValueError:
                                    png_extra+=1
                            while not scale_done:
                                scale_key=generate_name_base(req_data['user'], req_data['field'], req_data['date'],req_data['index_name']+'_scale',png_extra,'png')
                                try:
                                    scale_s.upload(scale_key)
                                    scale_key = scale_s.get_url()
                                    scale_done = True
                                except ValueError:
                                    scale_extra+=1
                            while not tif_done:
                                tif_key=generate_name_base(req_data['user'], req_data['field'], req_data['date'],req_data['index_name'],tif_extra,'tif')
                                try:
                                    tif_s.upload(tif_key)
                                    tif_key = tif_s.get_url()
                                    tif_done = True
                                except ValueError:
                                    tif_extra+=1
                        os.remove(png+'.aux.xml')
                        data = {'available':1,'png':png_key, 'bounds':bounds,'scale':scale_key}
                    max_id=sql_cursor.execute('SELECT MAX(id) FROM ami_api_overlayimage')
                    #print(max_id)
                    max_id = [_ for _ in max_id][0]
                    #print(max_id)
                    
                    max_id=(max_id[0] if max_id[0] else 0)+1
                    #print(max_id)
                    sql_cursor.execute('INSERT INTO ami_api_overlayimage (id, user, field, index_name, date, filepath, tiffilepath, scalefilepath) VALUES (?,?,?,?,?,?,?,?);',
                                        [max_id, req_data['user'],req_data['field'], req_data['index_name'],req_data['date'],png_key, tif_key, scale_key])
                    sql.commit()
                    del sql
                else:
                    #there is no available data and the default response will send
                    return HttpResponse(status=404)
            else:
                #read filepaths from sql_init_response
                png=sql_init_response[0][5]
                with S3GetHandler(sql_init_response[0][7],IMAGE_STORAGE) as tiff:
                    bounds = get_tif_bbox(tiff.tempname)
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


