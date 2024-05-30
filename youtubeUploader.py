#!/usr/bin/python
import os
from os import walk
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from supabase_rest_req import RestClient
from dotenv import load_dotenv


class YoutubeUploader:

    VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
    VALID_VIDEO_CATEGORIES = ("public", "private", "unlisted")

    def __init__(self, api_url: str, soko_api_key: str):
        load_dotenv()
        filecloud_dir = os.getenv('FILECLOUD_DIR')
        video_dir = filecloud_dir + os.getenv('VIDEO_APENDIX')
        channel_credentials = '{credentials: "token"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        video_json = '{filename: "1.mp4"}' ### REPLACE FOR INFORMATION FROM SUPABASE DATA
        print(channel_credentials)
        print(video_dir)
        print(video_json)
        #youtube_upload(video_dir, video_json, channel_credentials)

    def my_supabase_result_processor(input_string, output_json, client_url, client_uuid):
        print("\n\n\n******   my_supabase_result_processor is running   ******\n")

        hashed_string = sha256(input_string.encode('utf-8')).hexdigest()
        #	hashed_string=input_string

        print("\n\n\n******   hash:   ", hashed_string, "******\n")
        output_string = output_json
        # output_string=json.dumps(output_json)
        print("\n\n\n******   output string:   ", output_string, "******\n")

        url: str = 'https://zqggxkcnwyewelkvajbp.supabase.co'  # os.environ.get("SUPABASE_URL")
        key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxZ2d4a2Nud3lld2Vsa3ZhamJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM5NzM4MTcsImV4cCI6MjAyOTU0OTgxN30.UE6BskNtqSqFt8woq8rRidcJn4KRt1s36Zwj9Zi9voM'  # os.environ.get("SUPABASE_KEY")
        soko_api: RestClient = RestClient(url, key)
        r = soko_api.sign_in_with_password("scheduler@sokovfx.com", "1Aqwert21#")
        soko_api.raw_post("scheduler_results", {"hash": hashed_string, "result": output_string, "url": client_url, "uuid": client_uuid})

        print("\n\n\n******   my_supabase_result_processor FINISHED   ******\n")


    def youtube_upload(video_dir, supabase_json):
        
        ############################################
        # Set up video description, and attributes  
        # so the video can be uploaded to youtube
        ############################################   
        vide_file_path = file_path=video_dir + supabase_json.filename
        if not os.path.exists(vide_file_path):
            exit("FILE DOES NOT EXISTS")
    
        # setting up the video that is going to be uploaded
        video = LocalVideo(vide_file_path)

        # setting snippet
        video.set_title("Title to load from supabase")
        video.set_description("Description of the video to load from supabase")
        video.set_tags(["relax", "work", "Quizq12H"]) 
        video.set_category(24)
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
        video = channel.upload_video(video)
        video.like()
        print(video.id)    