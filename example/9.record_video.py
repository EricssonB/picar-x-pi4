from time import sleep, strftime, localtime
from vilib import Vilib
import readchar
import os
import sys

manual = '''
Press keys on keyboard to control recording:
    Q: Start / Pause / Continue
    E: Stop and Save
    Ctrl + C: Quit
'''

def print_overwrite(msg, end='', flush=True):
    print('\r\033[2K', end='', flush=True)
    print(msg, end=end, flush=True)

def main():
    rec_flag = 'stop' # start, pause, stop
    vname = None
    
    # Use a direct path to avoid permission issues
    username = os.getlogin()
    save_path = f"/home/{username}/picar-x/videos/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    Vilib.rec_video_set["path"] = save_path

    # Optimization: local=False prevents the Pi from freezing 
    # while trying to draw a window you can't see.
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)
    
    print("Initializing camera...")
    sleep(2.0)  # Wait for camera sensor to stabilize

    print(manual)
    print(f"Videos will be saved to: {save_path}")

    try:
        while True:
            key = readchar.readkey()
            key = key.lower()
            
            # Start / Pause Logic
            if key == 'q':
                if rec_flag == 'stop':
                    rec_flag = 'start'
                    vname = strftime("%Y-%m-%d-%H.%M.%S", localtime())
                    Vilib.rec_video_set["name"] = vname
                    Vilib.rec_video_run()
                    Vilib.rec_video_start()
                    print_overwrite('● RECORDING STARTED...')
                elif rec_flag == 'start':
                    rec_flag = 'pause'
                    Vilib.rec_video_pause()
                    print_overwrite('‖ PAUSED')
                elif rec_flag == 'pause':
                    rec_flag = 'start'
                    Vilib.rec_video_start()
                    print_overwrite('● CONTINUING...')
            
            # Stop Logic
            elif key == 'e' and rec_flag != 'stop':
                rec_flag = 'stop'
                Vilib.rec_video_stop()
                print_overwrite(f"✔ Saved: {vname}.avi", end='\n')
            
            # Manual Quit
            elif key == '\x03':  # Ctrl+C
                break

            sleep(0.1)
            
    finally:
        Vilib.camera_close()
        print('\nCamera closed. Quitting.')

if __name__ == "__main__":
    main()