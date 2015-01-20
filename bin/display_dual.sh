#!/bin/sh

function dual_work ()
{
    xrandr --output eDP1 --mode 2560x1600 \
           --output DP1 --mode 2560x1440 --scale 1.5x1.5 --right-of eDP1 --primary \
           --output HDMI2 --off \
           --output HDMI1 --off \
           --output DP2 --off \
           --output VIRTUAL1 --off
}

dual_work

# 'fixes' mouse
xrandr --output DP1 --panning 3840x2160

# normal
xrandr --output VIRTUAL1 --off \
       --output eDP1 --mode 2560x1600 --pos 0x0 --rotate normal \
       --output DP1 --off \
       --output HDMI2 --off \
       --output HDMI1 --off \
       --output DP2 --off


# And finally now this works
dual_work
