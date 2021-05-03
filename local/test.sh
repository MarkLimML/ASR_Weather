#!/bin/bash

for i in $(seq 1 100); do
    sleep 2 
    echo $i
done | whiptail --title 'Test script' --gauge 'Running...' 6 60 0