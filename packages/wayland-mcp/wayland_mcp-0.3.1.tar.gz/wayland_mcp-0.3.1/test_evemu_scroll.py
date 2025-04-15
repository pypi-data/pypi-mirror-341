"""Test script for mouse scroll using MouseController."""
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "wayland_mcp"))
from wayland_mcp.mouse_utils import MouseController

if __name__ == "__main__":
    mouse = MouseController()
    print("Scrolling down by 3 units...")
    mouse.scroll(-3)
    time.sleep(1)
    print("Scrolling up by 3 units...")
    mouse.scroll(3)
    print("Scroll test completed - please verify visually.")
