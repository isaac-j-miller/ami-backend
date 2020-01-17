# ami-backend
Django back end for the AMI web app

example image overlay request is: 
http://localhost:8000/overlays/req/request_overlay/?user=isaacmiller&field=Blenheim&date=2019-10-06&index_name=ndvi
(assuming locally hosting)
to get an NDVI overlay, scale, and metadata for the user isaacmiller's field Blenheim on the date October 6, 2019.

Requires Sqlite3 installed and the following Python packages:
django
rest_framework
osgeo/gdal
numpy
matplotlib
pillow
glob
shutil
Metashape (must go to https://www.agisoft.com/downloads/installer/ to download the .whl)
