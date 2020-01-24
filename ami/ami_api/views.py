from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
from .customutils import *
from rest_framework import viewsets, request
import ImageTools.index_generator as ig
from ImageTools.stitchSet import StitchSet as ss
import ImageTools.utils as imutils
from ImageTools.metashape_stitcher import stitch as stitch
from .serializers import *
from .models import *
import zipfile
import glob
import platform

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
        
        resp =sql_cursor.execute('SELECT latitude, longitude FROM ami_api_field WHERE user=? AND name=?',[user,field]).fetchone()
        return {'latitude':resp[0],'longitude':resp[1]}
        


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
                resp=[_ for _ in resp]
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
                                        [req_data['user'],req_data['field'],req_data['date'],req_data['index_name'].lower()])
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
                        if req_data['index_name'].lower()=='rgb':
                            tif = stitch.exportRGBAImage()
                            png=imutils.convert(tif,tif.replace('.tif','.png'))
                            bounds = get_tif_bbox(tif)
                            scale_key='na'
                            with S3PutHandler(png) as png_s, S3PutHandler(tif) as tif_s:
                                png_key=png_s.proper_upload(req_data['user'], req_data['field'], req_data['date'],req_data['index_name'].lower(),0,'png')
                                tif_key=tif_s.proper_upload(req_data['user'], req_data['field'], req_data['date'],req_data['index_name'].lower(),0,'tif')
                        else:
                            stitch.generateIndex(req_data['index_name'].lower())
                            tif, scale = stitch.exportGeneratedIndicesAsColorImages()[0]
                            png=imutils.convert(tif,tif.replace('.tif','.png'))
                            bounds = get_tif_bbox(tif)
                            with S3PutHandler(png) as png_s, S3PutHandler(scale) as scale_s, S3PutHandler(tif) as tif_s:
                                png_key=png_s.proper_upload(req_data['user'], req_data['field'], req_data['date'],req_data['index_name'].lower(),0,'png')
                                tif_key=tif_s.proper_upload(req_data['user'], req_data['field'], req_data['date'],req_data['index_name'].lower(),0,'tif')
                                scale_key=scale_s.proper_upload(req_data['user'], req_data['field'], req_data['date'],req_data['index_name'].lower()+'_scale',0,'png')
                        try:
                            os.remove(png+'.aux.xml')
                        except Exception as e:
                            print(e)
                        
                        data = {'available':1,'png':png_key, 'bounds':bounds,'scale':scale_key}
                    max_id=sql_cursor.execute('SELECT MAX(id) FROM ami_api_overlayimage')
                    #print(max_id)
                    max_id = [_ for _ in max_id][0]
                    #print(max_id)
                    
                    max_id=(max_id[0] if max_id[0] else 0)+1
                    #print(max_id)
                    sql_cursor.execute('INSERT INTO ami_api_overlayimage (id, user, field, index_name, date, filepath, tiffilepath, scalefilepath) VALUES (?,?,?,?,?,?,?,?);',
                                        [max_id, req_data['user'],req_data['field'], req_data['index_name'].lower(),req_data['date'],png_key, tif_key, scale_key])
                    sql.commit()
                    
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


class RawImageSetViewSet(viewsets.ModelViewSet):
    queryset = RawImageSet.objects.all().order_by('date')
    serializer_class = RawImageSetSerializer
    @action(methods=['get'], detail=True)
    def process(self,httprequest: HttpRequest, pk=None):
        if httprequest.method == 'GET':
            print('process request received')
            req_data = httprequest.GET.dict()
            print(req_data)
            
            with S3GetHandler(req_data['url'],IMAGE_STORAGE) as zipped:
                print('downloaded zip')
                
                files=os.listdir(IMAGE_STORAGE)
                done = False
                while not done:
                    fname=''.join(random.choices(LETTERS,k=10))
                    done = fname not in os.listdir(IMAGE_STORAGE)
                folder=os.path.join(IMAGE_STORAGE,fname)
                system = platform.system()
                os.mkdir(folder)
                print('unzipping')
                if system =='Windows':
                    print(subprocess.check_output(['tar','-zxvf','"'+zipped.tempname+'"','-C','"'+folder+'"']))
                elif system == 'Linux':
                    print(subprocess.check_output(['unzip','"'+zipped.tempname+'"','-d','"'+folder+'"']))
                else:
                    print('unsupported os')
                
                subs=glob.glob(os.path.join(folder,'****SET'))
                if not subs:
                    subs = [folder]
                else:
                    subs = [os.path.join(folder, sub) for sub in subs]
                print('stitchsets:',subs)
                orthos=[]
                dsms=[]
                print(len(subs), 'image sets detected')
                for sub in subs:
                #the file has now been extracted to directory
                #update bands so that this works with non-altum also
                    names = stitch(sub,req_data['bands'].split(','),'temp',IMAGE_STORAGE)
                    dsms.append(names[0])
                    orthoSize = os.path.getsize(names[1])
                    maxSize=40e6 # 40 MB
                    if orthoSize>maxSize:
                        orthos.append(ig.resize_tif(names[1],IMAGE_STORAGE,'temp_ortho_resized.tif',(maxSize/orthoSize)**.5))
                    print(names)
                if len(subs)>1:
                    outortho=os.path.join(IMAGE_STORAGE,'merged_ortho.tif')
                    outdsm=os.path.join(IMAGE_STORAGE,'merged_dsm.tif')
                    print('merging sets')
                    subprocess.check_output(['gdal_merge.py','-o', outortho,'-of','GTiff', ' '.join(orthos)])
                    subprocess.check_output(['gdal_merge.py','-o', outdsm,'-of','GTiff', ' '.join(dsms)])
                    ortho, dsm = outortho, outdsm
                else:
                    ortho, dsm = orthos[0], dsms[0]

                with S3PutHandler(dsm) as dsm_s, S3PutHandler(ortho) as ortho_s:
                    print('handler entered')
                    dsm_key=dsm_s.proper_upload(req_data['user'], req_data['field'], req_data['date'],'dsm',0,'tif')
                    ortho_key=ortho_s.proper_upload(req_data['user'], req_data['field'], req_data['date'],'ortho',0,'tif')
                    print('keys generated, ortho:',ortho_key,'dsm:',dsm_key)
                    sql = sqlite3.connect('./db.sqlite3')
                    sql_cursor = sql.cursor()
                    max_id=sql_cursor.execute('SELECT MAX(id) FROM ami_api_stackedimage')
                    #TODO: include error handling in case there are zero entries in the table
                    max_id = [_ for _ in max_id][0]
                    max_id=(max_id[0] if max_id[0] else 0)+1
                    sql_cursor.execute('INSERT INTO ami_api_stackedimage (id, user, field, date, filepath, demfilepath) VALUES (?,?,?,?,?,?)',[
                        max_id, req_data['user'], req_data['field'], req_data['date'], ortho_key, dsm_key
                    ])
                    sql.commit()
                    box = get_tif_bbox(dsm)
                    lat = (box[1]+box[3])/2
                    lon = (box[0]+box[2])/2
                    max_id=sql_cursor.execute('SELECT MAX(id) FROM ami_api_field')
                    #TODO: include error handling in case there are zero entries in the table
                    max_id = [_ for _ in max_id][0]
                    max_id=(max_id[0] if max_id[0] else 0)+1
                    sql_cursor.execute('INSERT INTO ami_api_field (id, name, user, latitude, longitude) VALUES (?,?,?,?,?)',[
                        max_id, req_data['field'],req_data['user'],lat, lon
                    ]
                    )
                #TODO: delete the zip file from the s3 bucket after processing.
                #TODO: clean up temporary files
                

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class IndexViewSet(viewsets.ModelViewSet):
    queryset = Index.objects.all().order_by('name')
    serializer_class = IndexSerializer
    @action(methods=['get'], detail=True)
    def request_indices(self,httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            resp =sql_cursor.execute('SELECT * FROM ami_api_index')
            
            return JsonResponse({index:{'long':long_name,'summary':summary} for index,long_name,summary in resp})
        else:
            return HttpResponse(status=400)

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all().order_by('name')
    serializer_class = FieldSerializer
    @action(methods=['get'], detail=True)
    def get_location(self,httprequest: HttpRequest, pk=None):
        sql = sqlite3.connect('./db.sqlite3')
        sql_cursor = sql.cursor()
        if httprequest.method == 'GET':
            req_data = httprequest.GET.dict()  
            resp =sql_cursor.execute('SELECT (latitude, longitude) FROM ami_api_field WHERE user="?" AND name = "?"',[req_data['user'],req_data['name']]).fetchone()
            
            return JsonResponse({'latitude':resp[0],'longitude':resp[1]})
        else:
            return HttpResponse(status=400) 