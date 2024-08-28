#PUBLISHER SERVICE 

Publisher service is publishing videos to youtube.

1) REQUIRES file sync service as GOOGLE DRIVE or FILECLOUD.
2) REQUIRES Dedicated SUPABASE DB project to read all metadata and configurations from.
3) CONFIGURE .env to identify path to folder, where the video files and thumbnails are synced by FILECLOUD
4) main.py contains script to run as a service on ubuntu machine


#video_api
1) In case you would like run an API use video_api.py
2) Configure GUNICORN service and NGINX
3) Get SSL CERTIFICATE
4) Create Post webhook in your database to call post requests to https://your_domain_name/api/v1/youtube/publish
