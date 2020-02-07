#FOR LINUX
#install external stuff
sudo apt install python3-pip
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install unzip
sudo apt-get install python3-gdal
sudo apt install gdal-bin
sudo apt install awscli
sudo apt install xterm
sudo apt-get install git-core git-gui git-doc
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt install nodejs
npm install react
npm install react-scripts
npm install aws-sdk
npm install react-dropzone
npm install -g serve
npm i serve
#install python libs
pip3 install -r requirements.txt
#configure github
git config --global user.name “isaac-j-miller”
git config --global user.email “miller.isaac96@gmail.com”
mkdir ~/git_repo
cd ~/git_repo
git init
git clone "https://github.com/isaac-j-miller/ami-backend"
