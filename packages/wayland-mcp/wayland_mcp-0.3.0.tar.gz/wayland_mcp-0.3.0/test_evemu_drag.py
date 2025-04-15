"""Test script for mouse drag using MouseController."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "wayland_mcp"))
from wayland_mcp.mouse_utils import MouseController

if __name__ == "__main__":
    mouse = MouseController()
    mouse.drag(350, 150, 1350, 150)
