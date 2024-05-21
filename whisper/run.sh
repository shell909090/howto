#!/bin/bash

for i in 2023/*
do
  echo $i
  time whisper --language Chinese --model large-v2 "$i"
done
