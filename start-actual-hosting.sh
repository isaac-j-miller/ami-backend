#ensure globals.js tells the front end to request from the actual host
cd ~/git_repo/ami-backend/ami-front/src
echo "export default {\n\tvalue: 'http://3.219.163.17:8000'\n}" > 'globals.js'
#turn debug mode on in django
cd ~/git_repo/ami-backend/ami
sed -i 's/"DEBUG_MODE\s?=\s?True"/"DEBUG_MODE = False"/g' > 'settings.py'
xterm -title 'backend server' -e 'python3 manage.py runserver 0.0.0.0:8000'
cd ~/git_repo/ami-backend/ami-front
xterm -title 'frontend server' -e 'npm start'