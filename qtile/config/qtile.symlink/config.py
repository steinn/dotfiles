import os
import re
import signal
import subprocess

from libqtile.config import Drag, Click, Key, Group
from libqtile.manager import Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook

mod_key = "mod4"
keys = [
    # Toggle between different layouts as defined below
    Key([mod_key], "space",    lazy.next_layout()),

    Key([mod_key], "j", lazy.layout.down()),
    Key([mod_key], "k", lazy.layout.up()),
    Key([mod_key], "Tab", lazy.layout.next()),
    Key([mod_key, "shift"], "Tab", lazy.layout.next()),
    Key([mod_key, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod_key, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod_key], "m", lazy.layout.maximize()),
    Key([mod_key], "n", lazy.layout.normalize()),

    # Key([mod_key], "Left", lazy.layout.grow()),
    # Key([mod_key], "m", lazy.layout.shrink()),

    # Key([mod_key, "shift"], "h", lazy.layout.swap_left()),
    # Key([mod_key, "shift"], "l", lazy.layout.swap_right()),
    # Key([mod_key], "h", lazy.layout.left()),
    # Key([mod_key], "l", lazy.layout.right()),
    # Key([mod_key], "f", lazy.layout.flip()),

    # Screen focus
    Key([mod_key], "e", lazy.to_screen(0)),
    Key([mod_key], "w", lazy.to_screen(1)),

    # Qtile controls
    Key([mod_key, "control"], "q", lazy.shutdown()),
    Key([mod_key, "control"], "r", lazy.restart()),
    Key([mod_key, "control"], "c", lazy.window.kill()),

    # Spawn commands
    Key([mod_key], "Return", lazy.spawn("urxvt")),
    Key([mod_key], "p", lazy.spawncmd()),

    # Volume
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -D pulse set Master 1%+")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("amixer -D pulse set Master 1%-")),
    Key([], "XF86AudioMute",
        lazy.spawn("amixer -D pulse set Master toggle")),

    # Backlight
    Key([], "XF86MonBrightnessUp", lazy.spawn(
        os.path.expanduser("~/.dotfiles/bin/light -A 5"))),
    Key([], "XF86MonBrightnessDown", lazy.spawn(
        os.path.expanduser("~/.dotfiles/bin/light -U 5"))),

    # Lock Screen
    Key([mod_key], "Escape", lazy.spawn(
        os.path.expanduser("~/.dotfiles/bin/lock_screen"))),

    # keyboard layout switch
    Key([mod_key], "i", lazy.widget["keyboardlayout"].next_keyboard())
]


groups = [Group(g) for g in "1234567890"]

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
    layout.verticaltile.VerticalTile()
]


widget_defaults = {
    "font": "Ubuntu Mono",
    "fontsize": 28,
    "padding": 3,
}

primary_widgets = [
    widget.CurrentScreen(),
    widget.GroupBox(padding=0, disable_drag=True),
    widget.CurrentLayout(),
    widget.TaskList(fontsize=20),
    widget.Prompt(),
    widget.CPUGraph(line_width=1.5,
                    width=150),
    widget.KeyboardLayout(configured_keyboards=["us", "is"]),
    widget.Volume(),
    widget.Battery(update_delay=5, foreground="#00ff00",
                   format=u"{char}{percent:2.0%} {hour:d}:{min:02d}",
                   discharge_char=u"\U00002193",  # ARROW DOWN
                   charge_char=u"\U00002191",     # ARROW UP
                   low_percentage=0.15),
    widget.Systray(icon_size=40, padding=2),
    widget.Clock(format='%H:%M:%S %d/%m'),
]

secondary_widgets = [
    widget.GroupBox(padding=0),
    widget.CurrentLayout(),
    widget.TaskList(fontsize=20),
    widget.Clock(format='%H:%M:%S %d/%m'),
]

primary_bar = bar.Bar(primary_widgets, 32)
secondary_bar = bar.Bar(secondary_widgets, 32)

screens = [
    Screen(top=primary_bar),
]
screens.append(Screen(top=secondary_bar))

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


def is_running(process):
    if isinstance(process, list):
        process = " ".join(process)
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False


def execute(process):
    if isinstance(process, str):
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
    #execute("rescuetime")


@hook.subscribe.startup
def startup():
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
    execute(["synclient", "PalmDetect=1"])

    xresource = os.path.expanduser("~/.dotfiles/bin/xresource")
    execute([xresource, "--color", "zenburn"])

    background = os.path.expanduser("~/.config/qtile/team-quizup_2560x1440-02.png")
    execute(["feh", "--bg-scale", background])
