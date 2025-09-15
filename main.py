#!/usr/bin/env python3

import sys
import os

def main():
    print("AI Project Verification System")
    print("=" * 40)
    print("Available commands:")
    print("  python verification_tool.py --mode cli")
    print("  python verification_tool.py --mode telegram")
    print("=" * 40)
    
    if os.path.exists("verification_tool.py"):
        print("Verification tool is ready!")
        print("Run: python verification_tool.py --mode cli")
    else:
        print("Verification tool not found!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())