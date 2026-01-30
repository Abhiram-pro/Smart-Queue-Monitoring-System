#!/usr/bin/env python3
import cv2
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 extract_frames.py <video_path> [output_dir] [num_frames]")
    sys.exit(1)

video_path = sys.argv[1]
output_dir = sys.argv[2] if len(sys.argv) > 2 else 'extracted_frames'
num_frames = int(sys.argv[3]) if len(sys.argv) > 3 else 10

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Cannot open video {video_path}")
    sys.exit(1)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Video: {video_path}")
print(f"Total frames: {total_frames}, FPS: {fps:.2f}")

# Extract frames evenly spaced
interval = max(1, total_frames // num_frames)
extracted = 0
frame_idx = 0

while cap.isOpened() and extracted < num_frames:
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_idx % interval == 0:
        out_path = os.path.join(output_dir, f'frame_{frame_idx:04d}.jpg')
        cv2.imwrite(out_path, frame)
        print(f"Extracted frame {frame_idx} -> {out_path}")
        extracted += 1
    
    frame_idx += 1

cap.release()
print(f"\nExtracted {extracted} frames to {output_dir}/")
