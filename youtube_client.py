#!/usr/bin/python
import os
from os import walk
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from supabase_rest_req import RestClient
from dotenv import load_dotenv


class youtube_client:
    filecloud_dir
    video_dir
    channel_data
    VALID_PRIVACY_STATUSES = ["public", "private", "unlisted"]
    VALID_VIDEO_CATEGORIES = [21, 22, 23]

    def load_channel_data(channel_id):
        print("\n\n\n******   load_channel_data is running and getting channel secrets from SUPABASE  ******\n")
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)
        channel_data_response = supa_api.raw_get("youtube_channel_credentials", 'id=eq.'+channel_id)
        print(channel_data_response)

    def update_video_status(video_id):
        print("\n\n\n******   update_video_status is running and updating video status to SUPABASE   ******\n")
        
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)
        supa_api.raw_post("youtube_video", '')
        print("\n\n\n******   update_video_status FINISHED   ******\n")

    def youtube_upload(video_data):
        
        ############################################
        # Set up video description, and attributes  
        # so the video can be uploaded to youtube
        ############################################   
        vide_file_path = file_path=video_dir + video_data['file_cloud_identifier']
        if not os.path.exists(vide_file_path):
            exit("FILE DOES NOT EXISTS")
    
        # setting up the video that is going to be uploaded
        video = LocalVideo(vide_file_path)

        # setting snippet
        video.set_title(video_data['youtube_title'])
        video.set_description(video_data['youtube_description'])
        video.set_tags(video_data['youtube_keywords'])
        video.set_category(video_data['youtube_category'])
        video.set_default_language("en-US")
    
        # setting status
        video.set_embeddable(True)
        video.set_license("creativeCommon")
        video.set_privacy_status(VALID_PRIVACY_STATUSES[0])
        video.set_public_stats_viewable(True)
        video.set_made_for_kids(True)    
    
        # setting thumbnail
        #video.set_thumbnail_path(thumbnail_dir + "\\"+ 'thumbnail_'+ question_type[1:].lower() +'_quiz_question_heigh.png')
    
        # loggin into the channel
        channel = Channel()
        channel.login("client_secrets_focus.json", "credentials.storage")
    
        # uploading video and printing the results
        video_response = channel.upload_video(video)
        video_response.like()
        print('Video was uploaded with following Youtube ID',video_response.id)
        return video_response
    
    def __init__(self, channel_id):
        print("initializing Youtube Uploader")
        load_dotenv()
        global filecloud_dir
        global video_dir
        global channel_data

        filecloud_dir = os.getenv('FILECLOUD_DIR')
        video_dir = filecloud_dir + os.getenv('CHANNEL_UPLOAD_FOLDER')
        channel_data = self.load_channel_data(channel_id)        
        print(video_dir)

        #video_json = '{filename: "1.mp4"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        #print(channel_credentials)
        #channel_credentials = '{credentials: "token"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        #print(video_json)
        #youtube_upload(video_dir, video_json, channel_credentials)        
