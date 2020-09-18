from flask import Flask, render_template, Response, jsonify, request
import cv2
import smtplib
import socket
import numpy
import time

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')





def gen_frames_c1():

    UDP_IP="127.0.0.1"
    UDP_PORT = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    s=""

    while True:
        data, addr = sock.recvfrom(46080)
        s+= data
        if len(s) == (46080*20):
            frame = numpy.fromstring (s, dtype=numpy.uint8)
            frame = frame.reshape(480,640,3)
            s=""
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames_c1(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)