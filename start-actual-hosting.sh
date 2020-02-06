#ensure globals.js tells the front end to request from the actual host
cd ~/git_repo/ami-backend/ami-front/src
echo $"export default {value: 'https://3.219.163.17:8000'}" > 'globals.js'
#turn debug mode off in django
cd ~/git_repo/ami-backend/ami/ami
sed -i 's/DEBUG\s?=\s?True/DEBUG = False/g' settings.py
cd ~/git_repo/ami-backend/ami
xterm -title 'backend server' -e 'gunicorn ami.wsgi' &
cd ~/git_repo/ami-backend/ami-front
npm run build
xterm -title 'frontend server' -e 'serve -s build' &
