#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import os
#Initialize the Flask app
app = Flask(__name__)
camera = cv2.VideoCapture("/dev/video0")

#if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
#    camera = cv2.VideoCapture(0)

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')


def gen_frames():
    #camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,use_reloader=True)
