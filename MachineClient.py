class MachineClient:
    """MachineClient class is a stub class for testing purposes. It is used to simulate machine operations."""

    def home(self):
        """ Moves machine to home position. """
        print("Moving to home.")

    def move(self, x, y, z):
        """ Uses linear movement to move spindle to given XYZ
        coordinates.
        Args:
        x (float): X axis absolute value [mm]
        y (float): Y axis absolute value [mm]
        z (float): Z axis absolute value [mm]
        """
        print("Moving to X={:.3f} Y={:.3f} Z={:.3f} [mm].".format(x, y,
        z))

    def move_x(self, value):
        """ Move spindle to given X coordinate. Keeps current Y and Z
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """
        print("Moving X to {:.3f} [mm].".format(value))

    def move_y(self, value):
        """ Move spindle to given Y coordinate. Keeps current X and Z
        unchanged.
        Args:
        value(float): Axis absolute value [mm]
        """
        print("Moving Y to {:.3f} [mm].".format(value))

    def move_z(self, value):
        """ Move spindle to given Z coordinate. Keeps current X and Y
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """
        print("Moving Z to {:.3f} [mm].".format(value))

    def set_feed_rate(self, value):
        """ Set spindle feed rate.
        Args:
        value (float): Feed rate [mm/s]
        """
        print("Using feed rate {} [mm/s].".format(value))

    def set_spindle_speed(self, value):
        """ Set spindle rotational speed.
        Args:
        value (int): Spindle speed [rpm]
        """
        print("Using spindle speed {} [mm/s].".format(value))



    def handle_gcode(self, gcode):
        """ Handles Gcode.
        Args:
        gcode (str): Gcode to handle.
        """

        gcode = int(gcode)

        match gcode:
            case 0:
                print("Using rapid positioning mode.")
            case 17:
                print("Using XY plane.")
            case 18:
                print("Using XZ plane.")
            case 19:
                print("Using YZ plane.")
            case 20:
                print("Using inches.")
            case 21:
                print("Using millimeters.")
            case 28:
                print("Returning to home position.")
            
            case 90:
                print("Using absolute positioning mode.")
            case 91:
                print("Using incremental positioning mode.")
            case default:
                print("Unknown gcode: {:d}.".format(gcode))

    def spindle_on(self):
        """ Turns spindle on. """
        print("Spindle turned on.")
    
    def spindle_off(self):
        """ Turns spindle off. """
        print("Spindle turned off.")

    def change_tool(self, tool_name):
        """ Change tool with given name.
        Args:
        tool_name (str): Tool name.
        """
        print("Changing tool '{:s}'.".format(tool_name))

    def coolant_on(self):
        """ Turns spindle coolant on. """
        print("Coolant turned on.")
    def coolant_off(self):
        """ Turns spindle coolant off. """
        print("Coolant turned off.")