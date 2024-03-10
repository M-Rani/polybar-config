#!/usr/bin/env bash

pkill polybar
polybar statusline 2>&1 | tee -a /tmp/polymain.log &
disown
~/.config/polybar/scripts/python-i3ipc.py &
disown
