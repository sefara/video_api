from flask import Flask, request, jsonify
from youtube_client import youtube_client

app = Flask(__name__)

@app.route('/')
def test1():
    print("FLASK TEST RUN OK")
    return ('Welcom to the PASSIVE API')

@app.route('/api/v1/integration/test', methods=['GET','POST'])
def test2():
	data = request.get_json()
	req_id=data['record']['id']
    
	text_to_return='TEST OK: Integration test - Value of Video ID: '+ str(req_id) + 'my data:' +data
	print(text_to_return)
	return (text_to_return)

@app.route('/api/v1/youtube/publish', methods=['GET','POST'])
def youtube_publish():
    #data = request.get_json()
    data = jsonify('{"my_sample:test", "record:"{"id=1","channel_id=1"}"}')
    print (data)
    
    if data is None or 'record' not in data or data['record'] is None or 'id' not in data['record'] or data['record']['id'] is None or 'channel_id' not in data['record'] or data['record']['channel_id'] is None :
         return 'Wrong request'
    channel_id = data['record']['channel_id']
    print (channel_id)
    video_data = data['record']
    
    my_client = youtube_client(channel_id)        
    video_processing_result = my_client.youtube_upload(video_data, channel_data)
    return 'Youtube publisher function finished'  

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()