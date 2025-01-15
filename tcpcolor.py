#!/usr/bin/env python3
import sys
import re
import signal
from datetime import datetime

# ANSI color codes
COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'CYAN': '\033[36m',
    'BOLD': '\033[1m',
    'RESET': '\033[0m'
}

def signal_handler(sig, frame):
    """Handle interrupt signals gracefully"""
    sys.stdout.flush()
    sys.exit(0)

def colorize_tcpdump(line):
    """Add color formatting to tcpdump output"""
    # Pattern to match IP addresses and ports
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    port_pattern = r'\.(\d+\s*[>:])'
    length_pattern = r'tcp (\d+)'
    
    # Add colors to IP addresses
    line = re.sub(ip_pattern, f"{COLORS['BLUE']}\g<1>{COLORS['RESET']}", line)
    
    # Add colors to ports
    line = re.sub(port_pattern, f".{COLORS['GREEN']}\g<1>{COLORS['RESET']}", line)
    
    # Add colors to packet length
    line = re.sub(length_pattern, f"length {COLORS['YELLOW']}\g<1>{COLORS['RESET']}", line)
    
    # Add timestamp
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    line = f"{COLORS['CYAN']}{timestamp}{COLORS['RESET']} {line}"
    
    return line

def format_output(line):
    """Format a single line of tcpdump output"""
    # Skip empty lines
    if not line.strip():
        return None
        
    try:
        return colorize_tcpdump(line)
    except Exception as e:
        return f"Error processing line: {e}"

def main():
    # Set up signal handlers
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # Handle broken pipe
    signal.signal(signal.SIGINT, signal_handler)    # Handle Ctrl+C

    # Disable output buffering
    sys.stdout.reconfigure(line_buffering=True)

    # Process stdin line by line
    while True:
        try:
            line = sys.stdin.readline()
            if not line:  # EOF
                break
                
            formatted = format_output(line.strip())
            if formatted:
                print(formatted, flush=True)
        except BrokenPipeError:
            sys.stderr.close()
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()
