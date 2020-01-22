#ensure globals.js tells the front end to request from the localhost
cd ~/git_repo/ami-backend/ami-front/src
echo $"export default {value:'http://127.0.0.1:8000'}" > 'globals.js'
#turn debug mode on in django
cd ~/git_repo/ami-backend/ami/ami
sed -i 's/DEBUG\s?=\s?False/DEBUG = True/g' settings.py
cd ~/git_repo/ami-backend/ami
xterm -title 'backend server' -e 'python3 manage.py runserver' &
cd ~/git_repo/ami-backend/ami-front
xterm -title 'frontend server' -e 'npm start' &
