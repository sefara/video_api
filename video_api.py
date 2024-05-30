from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def test1():
    print("FLASK TEST RUN OK")
    return ('Welcom to the PASSIVE API')

@app.route('/api/v1/passive/test2', methods=['POST'])
def test2():
#	req_id = request.args.get('req_id', default=0, type = int)
	data = request.get_json()
	print (data)
	req_id = data['record']['id']
	text_to_return = 'Hello world test '+ str(req_id)
	print(text_to_return)
	return (text_to_return)

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()