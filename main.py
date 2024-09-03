import json
import os
import time
from dotenv import load_dotenv
from youtube_client import YoutubeClient
from signal_handler import SignalHandler
from supabase_rest_req import RestClient


my_signal_handler = SignalHandler()

def check_supabase_youtube_videos():
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
        counter = 0
        for x in response:
            counter = counter + 1
            video_metadata = x
#            print("****DEBUG: VIDEO METADATA: ",video_metadata)
#            r2 = supa_api.raw_patch("youtube_video", "id=eq."+str(x['id']), json_data)
            update_video_metadata_in_supabase("status", "In Progress")
            youtube_id = youtube_publish()
            
            update_video_metadata_in_supabase("youtube_id", youtube_id)
                        
            update_video_metadata_in_supabase("status", "DONE")

        print("\n******   supabase_loader FINISHED round. Ammount of processed videos :", counter)


def update_video_metadata_in_supabase(attribute, value):
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
    video_id = my_client.youtube_upload(video_metadata, channel_data)    
    
    video_file_path = os.path.join(os.environ.get('VIDEO_ROOT_DIR'),channel_data['channel_dir'],  video_metadata['file_identifier'])
    archive_video_file_path = os.path.join(os.environ.get('ARCHIVE_ROOT_DIR'),channel_data['channel_dir'],  video_metadata['file_identifier'])
    thumbnail_file_path = os.path.join(os.environ.get('VIDEO_ROOT_DIR'),channel_data['channel_dir'],  video_metadata['thumbnail_identifier'])
    archive_thumbnail_file_path = os.path.join(os.environ.get('ARCHIVE_ROOT_DIR'),channel_data['channel_dir'],  video_metadata['thumbnail_identifier'])

    os.replace(video_file_path, archive_video_file_path)
    os.replace(thumbnail_file_path, archive_thumbnail_file_path)
    
    return video_id

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
    counter = 0
    while my_signal_handler.can_run():
        counter = counter + 1
        print("Up and running...")
        check_supabase_youtube_videos()
        create_watchdog_log_record = counter % 10
        if create_watchdog_log_record == 0:
            log_watchdog("video_publisher")
        time.sleep(10)
        
