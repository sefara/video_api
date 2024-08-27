import json
from supabase_rest_req import RestClient
from dotenv import load_dotenv
import os

def load_channel_data(channel_id):
        global channel_data
        print("\n\n\n******   load_channel_data is running and getting channel secrets from SUPABASE  ******\n")
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_ANON")
        user: str = os.environ.get("SUPABASE_USER")
        password: str = os.environ.get("SUPABASE_USER_PWD")
        supa_api: RestClient = RestClient(url, key)
        r = supa_api.sign_in_with_password(user, password)

        channel_data_response = supa_api.raw_get("youtube_channel_credentials", "*","id=eq."+str(channel_id))
        if (channel_data_response) is None:
            return None
        channel_data = channel_data_response[0]
        print(channel_data_response)
        print(channel_data)

def main():
	print("TEST OK: Simple python3 script with basic imports")
    

if __name__ == "__main__":
    load_dotenv()
    main()
    load_channel_data(3)