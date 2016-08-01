#!/bin/bash

# xrandr --output eDP1 --off \
#        --output HDMI2 --preferred

# xrandr --output eDP1 --preferred \
#        --output HDMI2 --off

xrandr --output HDMI2 --mode 2560x1440 --right-of eDP1 --scale 1.25x1.25 --primary \
       --output eDPI1 --preferred

xrandr --output HDMI2 --panning 3840x2160/3840x2160x0x0

xrandr --output eDP1 --off \
       --output HDMI2 --off

xrandr --output eDP1 --preferred \
       --output HDMI2 --off

xrandr --output HDMI2 --mode 2560x1440 --right-of eDP1 --scale 1.25x1.25 --primary \
       --output eDPI1 --preferred
