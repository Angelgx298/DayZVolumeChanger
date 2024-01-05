from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import keyboard

print("Programa en ejecucion")

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))

# Creo una coleccion de las aplicaciones con volumen
sessions = AudioUtilities.GetAllSessions()

# Variable para controlar el estado del volumen
current_volume = 0.3

for session in sessions:
    # Volumen de la sesion en especifico
    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
    if session.Process and session.Process.name() == "DayZ_x64.exe":
        volume.SetMasterVolume(current_volume, None)


# Función para alternar el volumen al pulsar la tecla "p"
def toggle_volume(e):
    global current_volume
    if current_volume == 0.3:
        current_volume = 1.0
    else:
        current_volume = 0.3

    # Aplicar el nuevo volumen a la sesión de DayZ
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "DayZ_x64.exe":
            volume.SetMasterVolume(current_volume, None)
            if current_volume == 1:
                print(f"El volumen se ha subido")
            else:
                print(f"El volumen se ha bajado")


# Asignar la función al evento de pulsar la tecla "p"
keyboard.on_press_key("p", toggle_volume)

# Tecla ñ termina el programa
keyboard.wait("ñ")
print("Fin del programa")
