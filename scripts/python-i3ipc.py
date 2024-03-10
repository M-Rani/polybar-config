#!/usr/bin/env python3

from i3ipc import Connection, Event
import subprocess

i3 = Connection()

class Primary_Area:
    x, y = [ 0, 0 ]
    def __init__(self, width, height):
        self.x = width + 1
        self.y = height + 1

class Polybar_Controller:
    w, h = [ 0, 0 ]
    x, y = [ 0, 0 ]
    def __init__(self):
        try:
            pro = subprocess.check_output('xdotool search --onlyvisible --classname polybar getwindowgeometry', shell=1).decode().split()
            geo, pos = pro[7].split('x'), pro[3].split(',')
            self.w, self.h = int(geo[0]), int(geo[1])
            self.x, self.y = int(pos[0]), int(pos[1])
        except:
            pass 

    def set_hook(self, name, n):
        subprocess.check_output('polybar-msg action "#{}.hook.{}"'.format(name, n), shell=1)

def set_indicator(i3, e):
    try: 
        polybar = Polybar_Controller()

        is_win_floating = 0
        for floating_status in [ "user_on", "auto_on" ]: 
            if e.container.floating == floating_status: is_win_floating = 1

        # if focused fails to be inititalized, reset indicator
        focused = i3.get_tree().find_focused()
        primary = Primary_Area(0 + focused.workspace().gaps.outer + 10, polybar.h + focused.workspace().gaps.outer + 10)

        if e.container.rect.x <= primary.x and e.container.rect.y <= primary.y and not is_win_floating:
            # polybar.set_hook("stack", 1)
            i3.command("mark Primary")
        else: 
            # polybar.set_hook("stack", 2)
            i3.command("mark Secondary")
        return
    except:
        Polybar_Controller().set_hook("stack", 0)
        for mark in [ "Primary", "Secondary" ]:
            [i3.command('unmark {}'.format(mark))]
        return

if __name__ == "__main__":
    i3.on('window::focus', set_indicator)
    i3.on('workspace::focus', set_indicator)

    i3.main()
