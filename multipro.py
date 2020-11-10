from pynput import keyboard
import multiprocessing
    

def key_process(keychar, is_pressed): 
    def on_release(key):
        is_pressed[keychar] = False
        print('release '+keychar)
        return False
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    #setup shared resource
    manager = multiprocessing.Manager()
    is_pressed = manager.dict()
    is_pressed['w'] = False
    is_pressed['a'] = False
    is_pressed['s'] = False
    is_pressed['d'] = False

    def on_press(key):
        keychar = key.char
        if is_pressed[keychar] == False:
            print("pressed "+keychar)
            is_pressed[keychar] = True
            multiprocessing.Process(target=key_process, args=[keychar, is_pressed]).start()
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()