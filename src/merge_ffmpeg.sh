#!/bin/bash
#merge the videos and audios depending of their respective name (intro.mp4 - intro.mp3)

VIDEO_DIR="/Volumes/REDBOXMEDIA_server/Design/RedBox Media/Mapping/MapManager/src/assets/video"
AUDIO_DIR="/Volumes/REDBOXMEDIA_server/Design/RedBox Media/Mapping/MapManager/src/audio/exports"

find "$VIDEO_DIR" -type f -name "*.mp4" | 
while read -r video_file; do 

  #get video name
  name=$(basename "${video_file%.*}")

  #setup file path from video name
  audio_file="${AUDIO_DIR}/${name}.mp3"

  #check if audio file exists
  if [[ -f "$audio_file" && -f "$video_file" ]]; then
    echo "Merging: $name"
    temp_file="${VIDEO_DIR}/temp_${name}.mp4"
    #merge audio and video and override existing videos
    ffmpeg -y -nostdin -i "$video_file" -i "$audio_file" -c:v copy -c:a aac "$temp_file" && mv "$temp_file" "$video_file" 
  fi

done
