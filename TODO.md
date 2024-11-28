Antes de iniciar. 
En el monitor.py en el array topics. comenta o agrega los topicos que escucharas, puedes escuchar todos, o desactivar los normales de departamentos para solo escuchar alertas.
actualmente esta comentado el topico departamentos y esta escuchando solo alertas. 
en settings json puedes cambiar la frecuencia de publicacion, para que no se sature, y puedes cambiar la probabilidad de fuga de agua. esta en 0.2, si quieres forzarla ponla en valores arriba del 50, la temperatura si quires forzar que se active baja el max y ajusta el umbral.

ANTES DE EJECUTAR MAIN.PY EJECUTA ESTO EN LA TERMINAL:

bypassear politicas en caso de que no te deje usar el venv: 
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

CREA EL VENV:
python -m venv venv
ó
py -m venv venv

EJECUTA EL VENV:
venv\Scripts\activate 

INSTALA PAHO-MQTT:
pip install paho-mqtt==1.6.1

VERIFICA QUE PAHO ESTE INSTALADO
pip show paho-mqtt

EJECUTA EL MAIN
py main.py
ó
python main.py


