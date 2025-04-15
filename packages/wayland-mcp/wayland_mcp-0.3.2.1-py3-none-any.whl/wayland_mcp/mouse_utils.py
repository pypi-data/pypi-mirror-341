"""MouseController using evemu-event for mouse actions on Linux."""
import subprocess
import time


class MouseController:
    """
    MouseController using evemu-event for mouse actions on Linux.
    Supports move, click, and reliable drag-and-drop with Wayland workarounds.
    """

    def __init__(self, device="/dev/input/event9"):
        """
        Initialize with the evemu device path.
        """
        self.device = device

    def _evemu(self, args):
        """
        Run an evemu-event command with the given arguments.
        """
        cmd = ["evemu-event", self.device] + args
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"evemu-event failed: {cmd} ({e})")
            return False

    def move_to(self, x, y):
        """
        Move mouse relative to current position using REL_X/REL_Y events.
        Args:
            x: Relative horizontal movement (pixels)
            y: Relative vertical movement (pixels)
        """
        self._evemu(
            ["--type", "EV_REL", "--code", "REL_X", "--value", str(x), "--sync"]
        )
        self._evemu(
            ["--type", "EV_REL", "--code", "REL_Y", "--value", str(y), "--sync"]
        )
        time.sleep(0.05)

    def move_to_absolute(self, x, y):
        """
        Move mouse to absolute screen coordinates by first resetting to (0,0).
        Args:
            x: Absolute horizontal position (pixels)
            y: Absolute vertical position (pixels)
        """
        # Reset to (0,0)
        self._evemu(
            ["--type", "EV_REL", "--code", "REL_X", "--value", "-5000", "--sync"]
        )
        self._evemu(
            ["--type", "EV_REL", "--code", "REL_Y", "--value", "-5000", "--sync"]
        )
        time.sleep(0.05)
        # Move to (x, y)
        self._evemu(
            ["--type", "EV_REL", "--code", "REL_X", "--value", str(x), "--sync"]
        )
        self._evemu(
            ["--type", "EV_REL", "--code", "REL_Y", "--value", str(y), "--sync"]
        )
        time.sleep(0.05)

    def click(self):
        """
        Perform a left mouse click at the current position.
        """
        self._evemu(
            ["--type", "EV_KEY", "--code", "BTN_LEFT", "--value", "1", "--sync"]
        )
        time.sleep(0.05)
        self._evemu(
            ["--type", "EV_KEY", "--code", "BTN_LEFT", "--value", "0", "--sync"]
        )

    def drag(self, x1, y1, x2, y2):
        """
        Perform a reliable drag-and-drop from (x1, y1) to (x2, y2).
        Decomposes the drag into two REL_X movements before releasing the button.
        """
        # Move to start
        self.move_to(x1, y1)
        time.sleep(0.1)
        # Mouse down
        self._evemu(
            ["--type", "EV_KEY", "--code", "BTN_LEFT", "--value", "1", "--sync"]
        )
        time.sleep(0.1)
        # Drag: move most of the way (REL_X dx-1, REL_Y dy)
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > 1:
            self._evemu(
                [
                    "--type",
                    "EV_REL",
                    "--code",
                    "REL_X",
                    "--value",
                    str(dx - 1),
                    "--sync",
                ]
            )
            self._evemu(
                ["--type", "EV_REL", "--code", "REL_Y", "--value", str(dy), "--sync"]
            )
            time.sleep(0.1)
            # Final REL_X=1, REL_Y=0
            self._evemu(
                ["--type", "EV_REL", "--code", "REL_X", "--value", "1", "--sync"]
            )
            self._evemu(
                ["--type", "EV_REL", "--code", "REL_Y", "--value", "0", "--sync"]
            )
            time.sleep(0.2)
        else:
            self._evemu(
                ["--type", "EV_REL", "--code", "REL_X", "--value", str(dx), "--sync"]
            )
            self._evemu(
                ["--type", "EV_REL", "--code", "REL_Y", "--value", str(dy), "--sync"]
            )
            time.sleep(0.2)
        # Mouse up
        self._evemu(
            ["--type", "EV_KEY", "--code", "BTN_LEFT", "--value", "0", "--sync"]
        )

    def scroll(self, amount):
        """
        Scroll vertically by the given amount (detents).
        Sends both REL_WHEEL and REL_WHEEL_HI_RES events for compatibility.
        """
        self._evemu(
            [
                "--type",
                "EV_REL",
                "--code",
                "REL_WHEEL",
                "--value",
                str(amount),
                "--sync",
            ]
        )
        self._evemu(
            [
                "--type",
                "EV_REL",
                "--code",
                "REL_WHEEL_HI_RES",
                "--value",
                str(amount * 120),
                "--sync",
            ]
        )
        time.sleep(0.1)
