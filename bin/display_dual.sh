#!/bin/sh
xrandr --output DP-2-1 --off \
       --output DP-2-2 \
         --primary \
         --mode 1920x1080 \
         --pos 2560x360 \
         --rotate normal \
       --output DP-2-3 --off \
       --output eDP-1 \
         --mode 2560x1440 \
         --pos 0x0 \
         --rotate normal \
       --output HDMI-2 --off \
       --output HDMI-1 --off \
       --output DP-2 --off \
       --output DP-1 --off

sleep 5

xrandr --output DP-2-2 --scale 1.5x1.5

sleep 5

xrandr --output DP-2-2 --panning 2880x1620+2560+360
