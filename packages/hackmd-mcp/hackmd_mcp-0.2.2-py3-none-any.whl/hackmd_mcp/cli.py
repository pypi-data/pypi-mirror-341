#!/usr/bin/env python3
"""
Command line interface for HackMD MCP.
"""
import argparse
import sys
from . import __version__

def main():
    """
    Main entry point for the command line interface.
    """
    parser = argparse.ArgumentParser(description="HackMD MCP - A command line utility for HackMD.")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # TODO: 在此添加您的命令行參數和功能
    # 例如：
    # parser.add_argument('command', choices=['upload', 'download'], help='Command to execute')
    # parser.add_argument('file', help='File to process')

    args = parser.parse_args()
    
    # TODO: 在此添加您的命令處理邏輯
    print("HackMD MCP is running!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
