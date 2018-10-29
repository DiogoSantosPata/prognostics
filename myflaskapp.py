from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import json
import numpy as np
from scipy import signal

app = Flask(__name__)
socketio = SocketIO(app)


# @socketio.on('message')
# def handle_json_button(json):
#     # it will forward the json to all clients.
#     print "IM in handle_json_button"
#     send(json, json=True)



def fft_welch(data):
	fs = 20	
	f, Pxx_den = signal.welch(data, fs, nperseg=1024)
	idx = np.argmax(Pxx_den)
	msg = "Peak freq: " + str( f[idx] ) + "   Amplitude: " + str(Pxx_den[idx])
	print msg
	

@socketio.on('my event', namespace='/test')
def test_message(message):
	print " im in test_message  ........... "
	print message
	# emit('my response', {'data': message['data']})


@app.route('/')
def display():
	# print request.namespace.socket.sessid    
	return render_template('index.html')


@app.route('/_array2python')
def array2python():
	print "im in array2python"

	## Get data
	sensor_data = json.loads(request.args.get('wordlist')) 
	## Parse data : find a better way to do this ... json it 
	sensor_data = sensor_data.split(':')[1]
	sensor_data = sensor_data[1:-2]
	sensor_data = sensor_data.split(',')
	sensor_data = np.array(sensor_data).astype(float)

	## Run fft on the sensor data 	
	fft_measure_msg = fft_welch(sensor_data)



	## Send FFT welch data back to javascript
	# test_message(fft_measure_msg)
	# handle_json_button(fft_measure_msg)


if __name__=='__main__':
	app.run(host='0.0.0.0', debug=False, port=3134)