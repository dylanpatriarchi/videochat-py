import cv2
import socketio
from flask import Flask, render_template
import base64
import io
from PIL import Image

app = Flask(__name__,template_folder='/home/rayoematto/Desktop/progetti/videochat-py')
sio = socketio.Server(cors_allowed_origins='*')
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

camera = cv2.VideoCapture(0) 

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('./index.html')

@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
