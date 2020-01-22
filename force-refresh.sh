cd ~/git_repo/ami-backend
git fetch origin master
git reset --hard FETCH_HEAD
git clean -df
cd ~/git_repo/ami_backend/ami
python3 manage.py makemigrations
python3 manage.py migrate