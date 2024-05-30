from flask import Flask, request, jsonify
from youtubeUploader import YoutubeUploader
#import json
#import os
#import uuid

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World'  

@app.route('/api/v1/youtube/publish')
def youtube_publish():
	
	my_uploader = YoutubeUploader()
	return 'Youtube publisher function'  

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()