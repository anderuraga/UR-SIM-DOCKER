# Imagen oficial URSim con VNC y noVNC

## 📥 Descargar la imagen

Ejecuta en tu terminal:

```
docker pull universalrobots/ursim_e-series
```

Esto descargará la versión más reciente de la imagen con URSim ya configurado.


Ejecuta el contenedor con puertos para VNC y noVNC:

```
docker run --rm -it -e ROBOT_MODEL=UR3 -p 5900:5900 -p 6080:6080 -p 30002:30002 -p 30003:30003 -p 30004:30004 universalrobots/ursim_e-series
```

```
# detalle de los puertos posibles
-p 5900:5900 \ # VNC
-p 6080:6080 \ # noVNC
-p 30002:30002 \ # URScript / RTDE
-p 30003:30003 \ # RTDE entrada/salida de datos
-p 30004:30004 \ # RTDE realtime
```

## Acceder a la GUI del simulador

Abre tu navegador y ve a:

http://localhost:6080/vnc.html




## 🚀 Ejecuta la AppWeb 

Ejecuta desde VSCode o comando el fichero app.py
Accede a la interfaz web de la app

http://localhost:5000/


> [!WARNING] 

Antes de poder probar la app debes entrar a la GUI del simulador y arrancar el robot 
Pulsando el boton START dos veces.
![ver imagen Captura.png](/captura.png)





> [!TIP]

## 💾 Persistir programas y cambios

Si quieres que los programas que crees en el simulador se guarden fuera del contenedor, monta un volumen:
Así los archivos de tu robot se quedan en tu carpeta local.

```
docker run --rm -it \
  -v "${HOME}/ursim_programs:/ursim/programs" \
  -p 5900:5900 -p 6080:6080 \
  universalrobots/ursim_e-series
```
