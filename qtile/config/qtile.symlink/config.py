import socket

from libqtile.config import Drag, Click, Key, Group
from libqtile.manager import Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook


HOSTNAME = socket.gethostname()
NET_INTERFACE = "wlp3s0" if HOSTNAME == "joggz" else "eth0"

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

    # Switch window focus to other pane(s) of stack
    Key([mod_key], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod_key, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout,
    # but still with multiple stack panes
    Key([mod_key, "shift"], "Return", lazy.layout.toggle_split()),

    Key([mod_key, "shift"], "a", lazy.layout.add()),
    Key([mod_key, "shift"], "d", lazy.layout.delete()),

    # xomand-tall key config
    # Key([mod_key], "i", lazy.layout.grow()),
    # Key([mod_key], "m", lazy.layout.shrink()),
    # Key([mod_key], "n", lazy.layout.normalize()),
    # Key([mod_key], "o", lazy.layout.maximize()),
    # Key([mod_key, "shift"], "space", lazy.layout.flip()),

    # Spawn commands
    Key([mod_key], "Return", lazy.spawn("urxvt")),
    Key([mod_key], "p", lazy.spawncmd()),

    # Screen focus
    Key([mod_key], "w", lazy.to_screen(1)),
    Key([mod_key], "e", lazy.to_screen(0)),

    # Misc
    Key([mod_key, "control"], "q", lazy.shutdown()),
    Key([mod_key, "control"], "r", lazy.restart()),
    Key([mod_key, "shift"], "c", lazy.window.kill()),

    # Volume
    Key([], "XF86AudioRaiseVolume", lazy.spawn("/usr/bin/vol_up")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("/usr/bin/vol_down")),
    Key([], "XF86AudioMute", lazy.spawn("/usr/bin/vol_toggle")),

    # Lock Screen
    Key([mod_key, "shift"], "l", lazy.spawn("$HOME/.dotfiles/bin/lock_screen")),
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
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod_key], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
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

widget_defaults = {"fontsize": 14,
                   "padding": 3,
                   "font": "Ubuntu Mono Bold"}

primary_widgets = [
    widget.GroupBox(padding=0),
    widget.sep.Sep(),
    widget.CurrentLayout(),
    widget.sep.Sep(),
    widget.WindowName(),
    widget.Prompt(),
    widget.CPUGraph(line_width=1.5),
    widget.MemoryGraph(graph_color="#ff0000",
                       line_width=1.5),
    widget.NetGraph(interface=NET_INTERFACE,
                    graph_color="#ffff00",
                    line_width=1.5),
    widget.sep.Sep(),
    widget.Volume(),
    widget.sep.Sep(),
    widget.Battery(update_delay=5, foreground="#00ff00"),
    widget.sep.Sep(),
    widget.Systray(),
    widget.sep.Sep(),
    widget.Clock('%H:%M:%S %d/%m/%y'),
]

if HOSTNAME == "joggz":
    primary_widgets.insert(6, widget.Wlan(interface="wlp3s0"))
    primary_widgets.insert(7, widget.sep.Sep())


secondary_widgets = [
    widget.GroupBox(padding=0),
    widget.sep.Sep(),
    widget.CurrentLayout(),
    widget.sep.Sep(),
    widget.WindowName(),
    widget.Clock('%H:%M:%S %d/%m/%y'),
]

primary_bar = bar.Bar(primary_widgets, 20)
seconadry_bar = bar.Bar(secondary_widgets, 20)

screens = [
    Screen(top=primary_bar),
    Screen(top=seconadry_bar),
]

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


#########
# Hooks #
#########

import os
import subprocess
import re


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

@hook.subscribe.startup
def startup():
    if HOSTNAME == "lt-h6-121023":
        execute_once("nm-applet")
        execute_once(["/home/steinn/.dotfiles/bin/dunst"])

    execute_once(["xscreensaver", "-no-splash"])


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
    execute(["wmname", "LG3D"])
    execute(["synclient", "PalmDetect=1"])

    xresources = os.path.expanduser("~/.Xresources")
    execute(["xrdb", "-merge", xresources])