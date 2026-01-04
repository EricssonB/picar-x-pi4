import sys
sys.path.append(r'/home/ericssonb/picar-x/lib')
from vilib import Vilib
import readchar
import os

manual = '''
Input key to call the function!
    q: Take photo
    1: Color detect : red
    2: Color detect : orange
    3: Color detect : yellow
    4: Color detect : green
    5: Color detect : blue
    6: Color detect : purple
    0: Switch off Color detect
    r: Scan the QR code
    f: Switch ON/OFF face detect
    s: Display detected object information
'''

def take_photo():
    import datetime
    now = datetime.datetime.now()
    name = now.strftime("%Y-%m-%d_%H-%M-%S")
    path = '/home/ericssonb/Pictures/'
    if not os.path.exists(path):
        os.makedirs(path)
    Vilib.take_photo(name, path)
    print(f'Photo saved to {path}{name}.jpg')

def face_detect(flag):
    if flag:
        Vilib.face_detect_switch(True)
        print('Face Detect: True')
    else:
        Vilib.face_detect_switch(False)
        print('Face Detect: False')

def main():
    flag_face = False
    color_list = ['close', 'red', 'orange', 'yellow', 'green', 'blue', 'purple']
    
    # Starting camera with the 320x240 resolution fix
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)
    
    print(manual)
    
    while True:
        key = readchar.readkey()
        key = key.lower()
        
        if key == 'q':
            take_photo()
        elif key == 'f':
            flag_face = not flag_face
            face_detect(flag_face)
        elif key in ('0', '1', '2', '3', '4', '5', '6'):
            index = int(key)
            if index == 0:
                Vilib.color_detect('close')
                print('Color detect: OFF')
            else:
                Vilib.color_detect(color_list[index])
                print(f'Color detect: {color_list[index]}')
        elif key == 'r':
            Vilib.qrcode_detect_switch(True)
            print('QR Code Detect: ON')
        elif key == 's':
            print(f'Detected objects: {Vilib.detect_obj_parameter}')
        elif key == '\x03': # Ctrl+C
            break

    Vilib.camera_close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Vilib.camera_close()
        sys.exit()