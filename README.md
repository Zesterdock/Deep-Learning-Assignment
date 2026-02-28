# Bag Counting using YOLOv8 and ByteTrack

## Overview
This project implements an automated bag counting system using:
- Custom-trained YOLOv8 model
- ByteTrack multi-object tracking
- Line-crossing logic for counting

## Features
- Custom dataset training
- Multi-scenario support
- Right-to-left conveyor detection
- Stable ID-based counting
- Video output with annotations

## Model Performance
- Precision: 82%
- Recall: 81%
- mAP50: 84%

## How to Run
pip install -r requirements.txt
python bag_counter.py
