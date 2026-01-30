#!/usr/bin/env python3
"""
Quick test script to verify alerts work with a short threshold
"""
import sys
import subprocess

# Run queue_analyzer with modified threshold
code = """
import sys
sys.path.insert(0, '.')

# Monkey-patch the threshold before importing
from queue_analyzer import QueueMonitor
QueueMonitor.ALERT_THRESHOLD_OVERRIDE = 20.0  # 20 seconds for testing

# Import main after patching
from queue_analyzer import main

# Override in __init__
original_init = QueueMonitor.__init__
def new_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    self.ALERT_THRESHOLD = 20.0
    print(f'\\n⚠️  TEST MODE: Alert threshold = {self.ALERT_THRESHOLD}s\\n')

QueueMonitor.__init__ = new_init

# Run main
sys.argv = ['queue_analyzer.py', 'test/queue_5.mp4', '--skip-drawing', '--zones-file', 'zones_temp.json']
main()
"""

result = subprocess.run(['python3', '-c', code], capture_output=False)
sys.exit(result.returncode)
