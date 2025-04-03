#!/bin/bash

for i in $2
do
  python3 run.py --execution-provider cuda --frame-processor {face_swapper,face_enhancer} --keep-fps --keep-audio --many-faces -s "$1" -t "$i" -o "$3"
done
