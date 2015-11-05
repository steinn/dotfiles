#!/bin/sh
# xrandr --output VIRTUAL1 --off \
#        --output eDP1 --mode 2560x1600 --scale 0.9x0.9 --pos 0x0 --rotate normal --primary \
#        --output DP1 --off \
#        --output HDMI2 --off \
#        --output HDMI1 --off \
#        --output DP2 --off


xrandr --output VIRTUAL1 --off \
       --output eDP1 --off \
       --output DP1 --off \
       --output HDMI2 --off \
       --output HDMI1 --off \
       --output DP2 --off

# --scale 0.9x0.9
xrandr --output VIRTUAL1 --off \
       --output eDP1 --mode 2560x1600 --pos 0x0 --rotate normal --primary \
       --output DP1 --off \
       --output HDMI2 --off \
       --output HDMI1 --off \
       --output DP2 --off
