"""Test script for mouse drag using MouseController."""
import sys
from pathlib import Path
from wayland_mcp.mouse_utils import MouseController

sys.path.append(str(Path(__file__).parent.parent))


def test_mouse():
    """Test mouse drag from (350, 150) to (1350, 150)."""
    mouse = MouseController()
    print("Testing drag from (350, 150) to (1350, 150)")
    mouse.mousemove(350, 150)
    print("Starting drag...")
    mouse.drag(350, 150, 1350, 150)
    print("Drag test completed - please verify")


if __name__ == "__main__":
    test_mouse()
