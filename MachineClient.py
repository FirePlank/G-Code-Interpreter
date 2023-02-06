class MachineClient:
    """MachineClient class is a stub class for testing purposes. It is used to simulate machine operations."""

    def move(self, x, y, z):
        """ Uses linear movement to move spindle to given XYZ
        coordinates.
        Args:
        x (float): X axis absolute value [mm]
        y (float): Y axis absolute value [mm]
        z (float): Z axis absolute value [mm]
        """
        print("Moving to X={} Y={} Z={} [mm].".format(x, y, z))

    def move_x(self, value):
        """ Move spindle to given X coordinate. Keeps current Y and Z
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """
        print("Moving X to {} [mm].".format(value))

    def move_y(self, value):
        """ Move spindle to given Y coordinate. Keeps current X and Z
        unchanged.
        Args:
        value(float): Axis absolute value [mm]
        """
        print("Moving Y to {} [mm].".format(value))

    def move_z(self, value):
        """ Move spindle to given Z coordinate. Keeps current X and Y
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """
        print("Moving Z to {} [mm].".format(value))

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

        # print a response depending on the gcode, in a real application this
        # would be used to control the machine
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
            case 40:
                print("Using tool radius compensation off.")
            case 41:
                print("Using tool radius compensation left.")
            case 42:
                print("Using tool radius compensation right.")
            case 43:
                print("Using tool length compensation.")
            case 49:
                print("Using tool length compensation off.")
            case 52:
                print("Setting coordinate system origin.")
            case 53:
                print("Using machine coordinates.")
            case 54:
                print("Using work coordinates.")
            case 80:
                print("Using cancel motion mode.")
            case 90:
                print("Using absolute positioning mode.")
            case 91:
                print("Using incremental positioning mode.")
            case 94:
                print("Using units per minute feed rate mode.")
            case default:
                print("Unknown gcode: {:d}.".format(gcode))

    def handle_mcode(self, mcode):
        """ Handles Mcode.
        Args:
        mcode (str): Mcode to handle.
        """

        mcode = int(mcode)

        match mcode:
            case 0:
                print("Stopping program.")
            case 1:
                print("Optional stop.")
            case 2 | 30:
                print("End of program.")
            case 3:
                print("Spindle on clockwise.")
            case 4:
                print("Spindle on counterclockwise.")
            case 5:
                print("Spindle stop.")
            case 6:
                print("Tool change.")
            case 7 | 8:
                print("Coolant on.")
            case 9:
                print("Coolant off.")
            case 10:
                print("Pallet clamp on.")
            case 11:
                print("Pallet clamp off.")
            case default:
                print("Unknown mcode: {:d}.".format(mcode))

    def change_tool(self, tool_name):
        """ Change tool with given name.
        Args:
        tool_name (str): Tool name.
        """
        print("Changing tool '{:s}'.".format(tool_name))
