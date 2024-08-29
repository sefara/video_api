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

    def update_channel_credentials_in_supabase(attribute, value, credentials_id):
        print("\n***DEBUG: update_youtube_video function started")

        load_dotenv()        
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)
        json_data = {
              attribute: value
        }
        response = supa_api.raw_patch("youtube_channel_credentials", "id=eq."+str(credentials_id), json_data)        
        print(response)
        print("\n\n\n****** updating_supabase FINISHED   ******\n")

    def youtube_upload(self, video_data, channel_data):
        load_dotenv()
        WORKING_DIR: str = os.environ.get("WORKING_DIR")

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

        video_file_path = os.path.join(os.environ.get('VIDEO_ROOT_DIR'),channel_data['channel_dir'],  video_data['file_identifier'])
        
        if not os.path.exists(video_file_path):            
            print("***DEBUG: FILE DOES NOT EXISTS: ", video_file_path)
            return ""

        # setting up the video that is going to be uploaded
        video = LocalVideo(video_file_path)

        # setting
        video.set_title(video_data['youtube_title'])
        video.set_description(video_data['youtube_description'])
        video.set_tags(video_data['youtube_keywords'].split(","))
        video.set_category(video_data['youtube_category'])

        # setting status
        video.set_default_language("en-US")
        video.set_embeddable(True)
        video.set_license("youtube")
        video.set_privacy_status("public")
        video.set_public_stats_viewable(True)
        video.set_made_for_kids(False)

        print (video)
        print('TODO: DOROBIT THUMBNAIL MANAGEMENT')
        # TODO: setting thumbnail
        # video.set_thumbnail_path(thumbnail_dir + "\\"+ 'thumbnail_'+ question_type[1:].lower() +'_quiz_question_heigh.png')
        credentials_file_path = os.path.join(WORKING_DIR,'credentials.json')
        credentials_to_store_file_path = os.path.join(WORKING_DIR,'credentials.to.store')
        client_secret_file_path = os.path.join(WORKING_DIR,'client_secret.json')

        if os.path.exists(credentials_file_path):
            os.remove(credentials_file_path)
        if os.path.exists(credentials_to_store_file_path):
            os.remove(credentials_to_store_file_path)
        if os.path.exists(client_secret_file_path):
            os.remove(client_secret_file_path)
            
        if channel_data is None or 'client_secret' not in channel_data or channel_data['client_secret'] is None or 'credentials' not in channel_data:
            return "No valid client_secret"

        with open(client_secret_file_path, 'w') as fa:
            json.dump(channel_data['client_secret'] , fa)  
        fa.close()
        channel = Channel()
       
        if channel_data['credentials'] is None:
            print("Credentials are NULL")               
            channel.login(client_secret_file_path, credentials_to_store_file_path,scope=SCOPES) 
            fb = open(credentials_to_store_file_path)               
            self.update_video_metadata_in_supabase("credentials", fb, video_data['id'])
        else:
            print("Credentials are OK")
            with open(credentials_file_path, 'w') as fc:
                json.dump(channel_data['credentials'] , fc)       
            fc.close()
            channel.login(client_secret_file_path, credentials_file_path)
            
        # loggin into the channel
#        channel = Channel()
#        channel.login('client_sercret.json', 'credentials.json')

        video_response = channel.upload_video(video)
        video_response.like()
        print('Video was uploaded with following Youtube ID', video_response.id)
     
        if os.path.exists(credentials_file_path):
            os.remove(credentials_file_path)
        if os.path.exists(credentials_to_store_file_path):
            os.remove(credentials_to_store_file_path)
        if os.path.exists(client_secret_file_path):
            os.remove(client_secret_file_path)
            
        return video_response.id
    
    def __init__(self):
        print("***DEBUG: initializing Youtube Uploader")
        
        # video_json = '{filename: "1.mp4"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        # print(channel_credentials)
        # channel_credentials = '{credentials: "token"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        # print(video_json)
        # youtube_upload(video_dir, video_json, channel_credentials
