#!/usr/bin/python
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from simple_youtube_api.youtube_constants import SCOPES
from supabase_rest_req import RestClient
from dotenv import load_dotenv
import os
import json


class YoutubeClient:
    
    VALID_PRIVACY_STATUSES = ["public", "private", "unlisted"]
    VALID_VIDEO_CATEGORIES = [21, 22, 23]

    def update_video_status(video_data, video_processing_result):
        print("\n\n\n******   update_video_status is running and updating video status to SUPABASE   ******\n")

        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)

        print('TODO: doplnit json')
        json_data = {
            "youtube_title": video_data['youtube_title'],
            "youtube_description": video_data['youtube_description'],
            "youtube_keywords": video_data['youtube_keywords'],
            "youtube_category": video_data['youtube_category'],
            "supa_server_role_key": video_data['supa_server_role_key']
        }
        response = supa_api.raw_patch(
            "youtube_video", "id=eq."+str(video_data['id']), json_data)
        print(response)

        supa_api.raw_post("youtube_video", '')
        print("\n\n\n******   update_video_status FINISHED   ******\n")

    def youtube_upload(self, video_data, channel_data):

        print (video_data)
        print ("\n\n\n\n\n\n")
        print (channel_data)
        if channel_data is None or 'channel_dir' not in channel_data or channel_data['channel_dir'] is None or video_data is None or 'file_identifier' not in video_data or video_data['file_identifier'] is None:
            print("***DEBUG: REQUIRED DATA DOES NOT EXISTS")
            return ""
        ############################################
        # Set up video description, and attributes
        # so the video can be uploaded to youtube
        ############################################

        vide_file_path = os.path.join(os.environ.get('VIDEO_ROOT_DIR'),channel_data['channel_dir'],  video_data['file_identifier'])
        
        if not os.path.exists(vide_file_path):            
            print("***DEBUG: FILE DOES NOT EXISTS: ", vide_file_path)
            return ""

        # setting up the video that is going to be uploaded
        video = LocalVideo(vide_file_path)

        # setting
        video.set_title(video_data['youtube_title'])
        video.set_description(video_data['youtube_description'])
        video.set_tags(video_data['youtube_keywords'].split(","))
        video.set_category(video_data['youtube_category'])

        # setting status
        video.set_default_language("en-US")
        video.set_embeddable(True)
        video.set_license("creativeCommon")
        video.set_privacy_status("public")
        video.set_public_stats_viewable(True)
        video.set_made_for_kids(False)

        print (video)
        print('TODO: DOROBIT THUMBNAIL MANAGEMENT')
        # TODO: setting thumbnail
        # video.set_thumbnail_path(thumbnail_dir + "\\"+ 'thumbnail_'+ question_type[1:].lower() +'_quiz_question_heigh.png')

        if os.path.exists('credentials.json'):
            os.remove('credentials.json')
        if os.path.exists('client_secret.json'):
            os.remove('client_secret.json')
            
        if channel_data is None or 'client_secret' not in channel_data or channel_data['client_secret'] is None or 'credentials' not in channel_data:
            return "No valid credentils"

        with open('/home/passive/video_api/client_secret.json', 'w') as fa:
            json.dump(channel_data['client_secret'] , fa)  
        fa.close()
        channel = Channel()
       
        if channel_data['credentials'] is None:
            print("Credentials are NULL")               
            channel.login('/home/passive/video_api/client_secret.json', '/home/passive/video_api/credentials.to.store',scope=SCOPES) 
            #scope="https://www.googleapis.com/auth/youtube.uploads")	
        else:
            print("Credentials are OK")
            with open('/home/passive/video_api/credentials.json', 'w') as fc:
                json.dump(channel_data['credentials'] , fc)       
            fc.close()
            channel.login('/home/passive/video_api/client_secret.json', '/home/passive/video_api/credentials.json')
        print("CONTINUE WITH CLIENT_SECRET")
      
        # loggin into the channel
#        channel = Channel()
#        channel.login('client_sercret.json', 'credentials.json')

        video_response = channel.upload_video(video)
        video_response.like()
        print('Video was uploaded with following Youtube ID', video_response.id)

        os.remove('client_sercret.json')
        os.remove('credentials.json')
        return video_response
    
    def __init__(self):
        print("***DEBUG: initializing Youtube Uploader")
        
        # video_json = '{filename: "1.mp4"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        # print(channel_credentials)
        # channel_credentials = '{credentials: "token"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        # print(video_json)
        # youtube_upload(video_dir, video_json, channel_credentials
