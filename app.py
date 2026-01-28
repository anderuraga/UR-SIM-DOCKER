from flask import Flask, render_template, redirect, url_for
import urx
import threading
import time

ROBOT_IP = "127.0.0.1"
ROBOT_PORT = 30002

app = Flask(__name__)

robot = None
robot_lock = threading.Lock()

def connect_robot():
    global robot
    if robot is None:
        print("Conectando al robot...")
        robot = urx.Robot(ROBOT_IP, ROBOT_PORT)
        time.sleep(0.5)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move")
def move_robot():
    global robot
    try:
        with robot_lock:
            connect_robot()
            home = [0.0, -0.5, 0.5, 0.0, 3.14, 0.0]
            robot.movej(home, acc=0.5, vel=0.2)
    except Exception as e:
        print("Error moviendo robot:", e)
    return redirect(url_for("index"))

@app.route("/stop")
def stop_robot():
    global robot
    try:
        with robot_lock:
            connect_robot()
            robot.stopj(acc=2.0)
    except Exception as e:
        print("Error parando robot:", e)
    return redirect(url_for("index"))

@app.route("/disconnect")
def disconnect():
    global robot
    with robot_lock:
        if robot:
            robot.close()
            robot = None
            print("Robot desconectado")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)