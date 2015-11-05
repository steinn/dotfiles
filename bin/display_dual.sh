#!/bin/sh

xrandr --output eDP1 --off \
       --output HDMI2 --preferred \

xrandr --output eDP1 --preferred \
       --output HDMI2 --off \

xrandr --output HDMI2 --mode 2560x1440 --right-of eDP1 --scale 1.5x1.5 --primary \

# 'fixes' mouse
xrandr --output HDMI2 --panning 3840x2160/3840x2160x0x0


xrandr --output eDP1 --off \
       --output HDMI2 --preferred \

xrandr --output eDP1 --preferred \
       --output HDMI2 --off \


xrandr --output HDMI2 --preferred  --right-of eDP1 --scale 1.5x1.5 --primary
