#!/bin/bash

source ~/bitcoin-venv/bin/activate

while true
do
    python3 supervision.py
    sleep 60
done
