#!/usr/bin/env bash

NOT_TIMER=10000 # in miliseconds
NOT_ID=$(pidof polybar)

FORMAT="%l:  %w \(%x\), %t\(%f\)"
CURR_LOC="$(timeout 1 curl -sS "https://ipinfo.io/city")"
CITY_LIST=(
  "${CURR_LOC// /+}"
  "Livermore"
  "Manteca"
)
# Remove possibly repeated elements
CITY_LIST=$(printf "%s\n" "$CITY_LIST[@]" | sort -u)

# Display notification without weather
NO_TITLE="$( date '+(%a) %b %d, %Y' )"
dunstify -r $NOT_ID -t $NOT_TIMER \
  "$NO_TITLE" \
  "$NO_BODY" 

# Get Current Location
for CITY in ${CITY_LIST[@]}; do 

  # Add weather to current if it runs successfully
  if WEATHER="$( timeout 3 curl -fGsS -H "Accept-Language: ${LANG%_*}" --compressed "https://wttr.in/${CITY// /+}?T&format=${FORMAT// /+}" )"; then
    NO_BODY+="$WEATHER\n"

  # Append notification if curl is successful
  dunstify -r $NOT_ID -t $NOT_TIMER \
    "$NO_TITLE" \
    "\n${NO_BODY/\\/ }" 
  fi

done
