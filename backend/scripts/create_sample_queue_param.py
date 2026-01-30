import numpy as np
import argparse
import os

# This script writes a simple queue_param .npy containing one or more rectangular regions.
# Each region is [x_min, y_min, x_max, y_max] in pixel coordinates.

parser = argparse.ArgumentParser(description='Create a sample queue_param numpy file')
parser.add_argument('--out', default='queue_param_demo.npy', help='Output .npy path')
parser.add_argument('--width', type=int, default=1280, help='Frame width (px)')
parser.add_argument('--height', type=int, default=720, help='Frame height (px)')
parser.add_argument('--mode', choices=['center','left','right'], default='center', help='Simple presets')
args = parser.parse_args()

w = args.width
h = args.height
if args.mode == 'center':
    # center queue box (approx center-bottom)
    boxes = [
        [int(w*0.35), int(h*0.45), int(w*0.65), int(h*0.95)]
    ]
elif args.mode == 'left':
    boxes = [
        [int(w*0.05), int(h*0.40), int(w*0.30), int(h*0.95)]
    ]
else:
    boxes = [
        [int(w*0.70), int(h*0.40), int(w*0.95), int(h*0.95)]
    ]

out_dir = os.path.dirname(args.out)
if out_dir:
    os.makedirs(out_dir, exist_ok=True)

np.save(args.out, np.array(boxes))
print(f"Wrote sample queue_param with {len(boxes)} box(es) to {args.out}")
