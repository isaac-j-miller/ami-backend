#ensure globals.js tells the front end to request from the localhost
cd ~/git_repo/ami-backend/ami-front/src
echo "export default {\n\tvalue:'http://127.0.0.1:8000'\n}" > 'globals.js'
#turn debug mode on in django
cd ~/git_repo/ami-backend/ami
sed -i 's/"DEBUG_MODE\s?=\s?False"/"DEBUG_MODE = True"/g' > 'settings.py'
xterm -title 'backend server' -e 'python3 manage.py runserver'
cd ~/git_repo/ami-backend/ami-front
xterm -title 'frontend server' -e 'npm start'
