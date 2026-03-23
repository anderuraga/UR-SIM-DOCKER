from flask import Flask, render_template, redirect, url_for, jsonify, request
import urx
import threading
import time
import sys, os

global stop_flag, is_moving

stop_flag = False
is_moving = False

#sys.stderr = open(os.devnull, "w")  # Ignora todos los mensajes de error C de URSim

ROBOT_IP = "127.0.0.1"
ROBOT_PORT = 30002


# ---- Función de movimiento seguro ----
def safe_movej(pos, acc=0.5, vel=0.2):
    global robot
    try:
        robot.movej(pos, acc=acc, vel=vel)
    except urx.urrobot.RobotException:
        pass  # Ignora Robot stopped o parsing warnings

# ---- Secuencia de movimientos ----
def move_robot_sequence():
    global stop_flag, is_moving
    is_moving = True
    positions = [
        (0, -1.0, 1.0, 0, 1.0, 0),
        (0, -0.8, 0.8, 0, 1.0, 0)
    ]
    for pos in positions:
        if stop_flag:
            is_moving = False
            return
        safe_movej(pos)
        time.sleep(2)
    is_moving = False

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


@app.route("/status", methods=["GET"])
def status():
    global robot
    try:
        if robot is None:
            return jsonify({
                "state": "Robot no conectado",
                "moving": False,
                "joints": [0]*6
            })

        joints = robot.getj()
        state = "Robot listo"
    except urx.urrobot.RobotException:
        joints = [0]*6
        state = "Robot detenido / E-STOP activo"

    return jsonify({
        "state": state,
        "moving": is_moving,
        "joints": [round(j, 4) for j in joints]
    })

if __name__ == "__main__":
    app.run(debug=True, threaded=True)