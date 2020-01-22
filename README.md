# ami-backend
Django back end for the AMI web app

example image overlay request is: 
http://localhost:8000/overlays/req/request_overlay/?user=isaacmiller&field=Blenheim&date=2019-10-06&index_name=ndvi
(assuming locally hosting)
to get an NDVI overlay, scale, and metadata for the user isaacmiller's field Blenheim on the date October 6, 2019.

there are a few shell scripts to help with the setup. To localhost, I recommend copy-pasting the text from install-dependencies.sh to your machine and replacing the github username and email with your own or commenting out the github config if it is already set up. Then, you must run 'aws configure' in the terminal and set that up with your appropriate aws credentials.

To start the local server, run start-local-hosting.sh 