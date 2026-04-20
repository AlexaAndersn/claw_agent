#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

try:
    from main import main
    print("Main import OK")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
