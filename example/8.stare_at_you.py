from picarx import Picarx
from time import sleep
from vilib import Vilib

px = Picarx()

def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))

def main():
    # Optimization 1: Start camera and ONLY display to web (disables local desktop window)
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True) 
    Vilib.face_detect_switch(True)
    
    x_angle = 0
    y_angle = 0
    
    print("Face tracking started. Open http://10.1.10.46:9000/mjpg")
    
    while True:
        # Optimization 2: Use human_n check but verify data exists
        if Vilib.detect_obj_parameter['human_n'] != 0:
            coordinate_x = Vilib.detect_obj_parameter['human_x']
            coordinate_y = Vilib.detect_obj_parameter['human_y']
            
            # Calculate new angles
            # 640x480 is the default resolution; we calculate center offset
            x_angle += (coordinate_x * 10 / 640) - 5
            x_angle = clamp_number(x_angle, -35, 35)
            px.set_cam_pan_angle(x_angle)

            y_angle -= (coordinate_y * 10 / 480) - 5
            y_angle = clamp_number(y_angle, -35, 35)
            px.set_cam_tilt_angle(y_angle)

            sleep(0.1) # Increased sleep slightly to allow video frames to send
        else:
            sleep(0.2) # Sleep longer when no face is seen to clear the CPU

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        px.stop()
        Vilib.camera_close() # Ensure camera is released
        print("stop and exit")