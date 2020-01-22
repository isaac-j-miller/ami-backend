#FOR LINUX
#install external stuff
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install python3-gdal
sudo apt install gdal-bin
sudo apt install python3-pip
sudo apt install awscli
sudo apt-get install git-core git-gui git-doc
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt install nodejs
npm install react
npm install react-scripts
#install python libs
pip3 install matplotlib
pip3 install wheel
pip3 install http://download.agisoft.com/Metashape-1.6.1-cp35.cp36.cp37-abi3-linux_x86_64.whl
pip3 install django
pip3 install pillow
pip3 install numpy
pip3 install django-cors-headers
pip3 install djangorestframework
pip3 install boto3
pip3 install awscli
pip3 install rasterio
#configure github
git config --global user.name “isaac-j-miller”
git config --global user.email “miller.isaac96@gmail.com”
mkdir ~/git_repo
cd ~/git_repo
git init
git clone "https://github.com/isaac-j-miller/ami-backend"
