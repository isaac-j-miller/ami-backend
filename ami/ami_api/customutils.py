import os, sqlite3, sys, subprocess
import json
import boto3
import random, string
from botocore.exceptions import ClientError

sys.path.append('..')
BUCKET='skyprecison'
IMAGE_STORAGE = os.path.abspath('./images')
OVERLAY_STORAGE = os.path.abspath('./images/overlays')
STITCH_STORAGE = os.path.abspath('./images/stitched')
LETTERS=list(string.ascii_letters)
CONTENT_TYPES={
    'png':'image/png',
    'jpeg':'image/jpeg',
    'tif':'image/tif'
}

def generate_name_base(user, field, date, kind, extra, extension):
    #TODO: make this generate an output filename base
    newDate=date.replace(' ','_').replace(':','_').replace('.','_').replace('-','_')
    return '{}_{}_{}_{}_{}.{}'.format(user, field, newDate,kind,extra,extension)

def get_tif_bbox(filename):
    answer=subprocess.check_output(['gdalinfo',filename,'-json'])
    jsonAnswer = json.loads(answer)
    left = jsonAnswer['cornerCoordinates']['upperLeft'][0]
    bottom = jsonAnswer['cornerCoordinates']['lowerLeft'][1]
    right = jsonAnswer['cornerCoordinates']['upperRight'][0]
    top = jsonAnswer['cornerCoordinates']['upperLeft'][1]
    print(filename, jsonAnswer['cornerCoordinates'])
    return [left, bottom, right, top]

def genS3path(bucket):
    return 'https://{}.s3.amazonaws.com/'.format(bucket)

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file. 
    Sourced from https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

class S3GetHandler:
    def __init__(self, s3url, tempdir):
        self.s3url=s3url
        self.tempdir=tempdir
        self.tempname=self._get_name()
        print('url:',s3url)
        print('tempname:',os.path.abspath(self.tempname))
        self.bucket = boto3.resource('s3').Bucket(BUCKET)
        self.bucket.download_file(self.s3url.replace(genS3path(BUCKET),''),self.tempname)
        
    
    def _get_name(self):
        filetype=self.s3url.split('.')[-1]
        files=os.listdir(self.tempdir)
        done = False
        while not done:
            fname='{}.{}'.format(''.join(random.choices(LETTERS,k=10)), filetype)
            done = fname not in os.listdir(self.tempdir)
        return os.path.join(self.tempdir, fname)

    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        os.remove(self.tempname)

class S3PutHandler:
    def __init__(self, fpath):
        self.fpath=fpath
        self.bucket = boto3.resource('s3').Bucket(BUCKET)
        self.key=None

    def upload(self, key, public_read=True):
        keys = [o.key for o in self.bucket.objects.all()]
        if key in keys:
            raise ValueError('Key already in bucket')
        else:
            self.bucket.upload_file(self.fpath,key)
            self.key=key
            if public_read:
                boto3.resource('s3').ObjectAcl(BUCKET, self.key).put(ACL='public-read')
    
    def get_url(self):
        if self.key is not None:
            return 'https://{}.s3.amazonaws.com/{}'.format(BUCKET, self.key)
        else:
            raise ValueError('Key has not been verified')
        
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        os.remove(self.fpath)

