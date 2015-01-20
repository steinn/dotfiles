import logging
import os

# logging.basicConfig(
#     level=logging.DEBUG, filename=os.path.expanduser("~/.qtile.log"))
# logging.getLogger("qtile").setLevel(logging.INFO)

from libqtile.config import Drag, Click, Key, Group
from libqtile.manager import Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget

#from system import get_num_monitors

#log = logging.getLogger("qtile.config")

# Find urxvt binary and if not found use xterm


mod_key = "mod4"
keys = [
    # Toggle between different layouts as defined below
    Key([mod_key], "Tab",    lazy.nextlayout()),

    # Switch between windows in current stack pane

    Key([mod_key], "k", lazy.layout.up()),
    Key([mod_key], "j", lazy.layout.down()),
    Key([mod_key, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod_key, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod_key, "control"], "k", lazy.layout.client_to_next()),
    Key([mod_key, "control"], "j", lazy.layout.client_to_previous()),

    # Stack Layout
    # Switch window focus to other pane(s) of stack
    Key([mod_key], "space", lazy.layout.next()),
    # Swap panes of split stack
    Key([mod_key], "l", lazy.layout.rotate()),
    # Toggle between split and unsplit sides of stack.
    Key([mod_key, "shift"], "Return", lazy.layout.toggle_split()),

    # Spawn commands
    Key([mod_key], "Return", lazy.spawn("urxvt")),
    Key([mod_key], "p", lazy.spawncmd()),

    # Screen focus
    Key([mod_key], "e", lazy.to_screen(0)),
    Key([mod_key], "w", lazy.to_screen(1)),

    # Misc
    Key([mod_key, "control"], "q", lazy.shutdown()),
    Key([mod_key, "control"], "r", lazy.restart()),
    Key([mod_key, "control"], "c", lazy.window.kill()),

    # Volume
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -D pulse set Master 1%+")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("amixer -D pulse set Master 1%-")),
    Key([], "XF86AudioMute",
        lazy.spawn("amixer -D pulse set Master toggle")),


    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight +2")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -2")),

    # Lock Screen
    Key([mod_key], "Escape", lazy.spawn("$HOME/.dotfiles/bin/lock_screen")),
]


groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9"),
    Group("0"),
    #Group("8", persist=False, init=False),
    # Group("9", persist=False, init=False),
]

for i in groups:
    # mod + letter of group = switch to group
    keys.append(
        Key([mod_key], i.name, lazy.group[i.name].toscreen())
    )

    # mod + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod_key, "shift"], i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    # layout.Floating(),
    # layout.MonadTall(),
    # layout.RatioTile(),
    # layout.Slice("left", 256),
    # layout.TreeTab(),
    # layout.Zoomy(),
]

widget_defaults = {
    "font": "Ubuntu Mono",
    "fontsize": 28,
    "padding": 3,
}

primary_widgets = [
    widget.GroupBox(padding=0),
    widget.CurrentLayout(),
    #widget.WindowName(),
    #widget.WindowTabs(),
    widget.TaskList(fontsize=20),
    widget.Prompt(),
    widget.CPUGraph(line_width=1.5,
                    width=150),
    widget.MemoryGraph(graph_color="#ff0000",
                       line_width=1.5,
                       samples=100,
                       width=150),
    widget.HDDBusyGraph(graph_color="#ffff00",
                        line_width=1.5,
                        width=150),
    widget.NetGraph(graph_color="#ffffff",
                    line_width=1.5,
                    width=75,
                    bandwith_type="down"),
    widget.NetGraph(graph_color="#ff00ff",
                    line_width=1.5,
                    width=75,
                    bandwidth_type="up"),
    widget.Volume(cardid=1),
    widget.Battery(update_delay=5, foreground="#00ff00",
                   format=u"{char}{percent:2.0%} {hour:d}:{min:02d}",
                   discharge_char=u"\U00002193",  # ARROW DOWN
                   charge_char=u"\U00002191",     # ARROW UP
                   low_percentage=0.15),
    widget.Systray(icon_size=40, padding=2),
    widget.Clock('%H:%M:%S %d/%m'),
]

secondary_widgets = [
    widget.GroupBox(padding=0),
    widget.CurrentLayout(),
    widget.TaskList(fontsize=20),
    widget.Clock('%H:%M:%S %d/%m'),
]

primary_bar = bar.Bar(primary_widgets, 32)
secondary_bar = bar.Bar(secondary_widgets, 32)

screens = [
    Screen(top=primary_bar),
]
screens.append(Screen(top=secondary_bar))
#if get_num_monitors() > 1:


main = None
follow_mouse_focus = True
cursor_warp = False
floating_layout = layout.Floating()

mouse = [
    Drag([mod_key], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod_key], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod_key], "Button2", lazy.window.bring_to_front())
]

import os
import signal

from libqtile import hook

import logging
import platform
import re
import subprocess

log = logging.getLogger("qtile.config.system")

hostname = platform.node()


def get_num_monitors():
    output = subprocess.Popen(
        'xrandr | grep -e "\ connected" | cut -d" " -f1',
        shell=True, stdout=subprocess.PIPE).communicate()[0]
    displays = output.strip().split('\n')
    #log.debug(displays)
    return len(displays)


def is_running(process):
    if isinstance(process, list):
        process = " ".join(process)
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False


def execute(process):
    if isinstance(process, basestring):
        process = process.split()
    return subprocess.Popen(process)


def execute_once(process):
    if not is_running(process):
        execute(process)


@hook.subscribe.startup_once
def startup_once():
    execute("xscreensaver -no-splash")
    execute("nm-applet")
    execute("dunst")
    execute("rescuetime")


@hook.subscribe.startup
def startup():
    # http://stackoverflow.com/questions/6442428/
    # how-to-use-popen-to-run-backgroud-process-and-avoid-zombie
    #signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # Toggle layout change with menu key and use caps lock led to
    # indicate what layout is on (on - is, off - us).
    # Set caps lock as left ctrl
    execute(["setxkbmap",
             "-layout", "us, is",
             "-option", "grp:menu_toggle",
             "-option", "ctrl:nocaps",
             "-option", "grp_led:caps"])

    # disable bell
    execute(["xset", "b", "off"])
    execute(["xsetroot", "-cursor_name", "left_ptr"])
    execute(["xsetroot", "-solid", "black"])
    #<execute(["wmname", "LG3D"])
    execute(["synclient", "PalmDetect=1"])

    xresource = os.path.expanduser("~/.dotfiles/bin/xresource")
    execute([xresource, "--color", "zenburn"])

# def main(self):
#     logging.basicConfig(
#         level=logging.DEBUG, filename=os.path.expanduser("~/.qtile.log"))
#     logging.getLogger("qtile").setLevel(logging.DEBUG)
#     logging.getLogger("qtile.themes").setLevel(logging.DEBUG)
#     logging.getLogger("qtile.config").setLevel(logging.DEBUG)
