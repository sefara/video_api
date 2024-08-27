import json
import os
import time
from dotenv import load_dotenv
from youtube_client import YoutubeClient
from signal_handler import SignalHandler
from supabase_rest_req import RestClient


my_signal_handler = SignalHandler()

def check_supabase():
#        print("\n***DEBUG: loading input data from supabase")
        load_dotenv()
        
        global video_metadata
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)

        response = supa_api.raw_get("youtube_video", "*", "status=is.null")        
        json_data = {
           "status": "in progress"
        }

        for x in response:       
            video_metadata = x
#            print("****DEBUG: VIDEO METADATA: ",video_metadata)
            r2 = supa_api.raw_patch("youtube_video", "id=eq."+str(x['id']), json_data)
            youtube_publish()
            print("\n\n\n******   supabase_loader FINISHED   ******\n")

def update_metadata_in_supabase(youtube_id):
        print("\n***DEBUG: update_youtube_video function started")

        load_dotenv()        
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)
        json_data = {
              "youtube_id": youtube_id
        }
        response = supa_api.raw_patch("youtube_video", "id=eq."+str(video_metadata['id']), json_data)        
        print(response)
        print("\n\n\n****** updating_supabase FINISHED   ******\n")

def load_channel_data():
        load_dotenv()               
        
        print("\n\n\n******   load_channel_data is running and getting channel secrets from SUPABASE  ******\n")
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)

        channel_data_response = supa_api.raw_get("youtube_channel_credentials", "*", "id=eq."+str(video_metadata['channel_id']))
        if (channel_data_response) is None:
            return None
        channel_data = channel_data_response[0]         
        
        #video_dir = os.environ.get('VIDEO_ROOT_DIR') + channel_data('channel_dir')

        #DEBUG
        #print("*****DEBUG VIDEO DIR: ", video_dir)
        #print("*****DEBUG CHANNEL DATA RESPONSE: ",channel_data_response)
        #print("*****DEBUG CHANNEL DATA RESPONSE: ",channel_data)
        #DEBUG
        return channel_data

def youtube_publish():    
    if video_metadata['channel_id'] is None:    
        return "error in processing: Channel ID is required"
    
    my_client = YoutubeClient()
    channel_data = load_channel_data()
#    print ("*******DEBUG: ",channel_data)
    video_processing_result = my_client.youtube_upload(video_metadata, channel_data)
    #video_processing_result = my_client.update_video_status(video_data, video_processing_result)
    return 'Youtube publisher function finished'

def log_watchdog(name):
        #print("\n***DEBUG: log watchdog function started")

        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)

        json_data = {
                "name": name
        }
        response = supa_api.raw_post("log_watchdog", json_data)        
        #print(response)
        #print("\n\n\n***DEBUG: log watcdog FINISHED   ******\n")


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    while my_signal_handler.can_run():
        print("Up and running...")
        check_supabase()
        log_watchdog("video_uploader")
        time.sleep(6)
        
