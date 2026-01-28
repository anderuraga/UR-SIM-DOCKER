###############################################
# Test rapido para ver que se mueve el robot
###############################################
# Recuerda entrar en la GUI y arrancar el robot
# pulsa boton START dos veces
# http://localhost:6080/vnc.html
################################################

import urx
import time

# Configuración del robot
ROBOT_IP = "127.0.0.1"  # localhost si es URSim
ROBOT_PORT = 30002       # puerto URScript

def main():
    try:
        print("Conectando al robot...")
        robot = urx.Robot(ROBOT_IP, ROBOT_PORT)
        print("Conexión establecida.")

        # Posición inicial (segura)
        home_position = [0.0, -0.5, 0.5, 0.0, 3.14, 0.0]
        print("Moviendo a posición inicial...")
        robot.movej(home_position, acc=0.5, vel=0.2)

        time.sleep(1)

        # Segunda posición (ejemplo)
        target_position = [0.3, -0.3, 0.4, 0.0, 3.14, 0.0]
        print("Moviendo a posición objetivo...")
        robot.movel(target_position, acc=0.3, vel=0.2)

        time.sleep(1)

        # Regresar a posición inicial
        print("Regresando a posición inicial...")
        robot.movej(home_position, acc=0.5, vel=0.2)

        print("Movimiento completado.")

    except Exception as e:
        print("Error:", e)
    finally:
        robot.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()