import struct as st

from thorlabs_cube.driver.message import MGMSG, Message, MsgError
from thorlabs_cube.driver.tcube.tdc import Tdc, TdcSim


class Kdc(Tdc):
    """
    KDC101 K-Cube Brushed DC Servo Motor Controller class
    """

    async def handle_message(self, msg: Message) -> None:
        """Parse messages from the device.
        Minor adaptation from TDC001 method."""
        msg_id = msg.id
        data = msg.data

        if msg_id == MGMSG.HW_DISCONNECT:
            raise MsgError("Error: Please disconnect the KDC101")
        elif msg_id == MGMSG.HW_RESPONSE:
            raise MsgError("Hardware error, please disconnect and reconnect the KDC101")
        elif msg_id == MGMSG.HW_RICHRESPONSE:
            (code,) = st.unpack("<H", data[2:4])
            raise MsgError(
                f"Hardware error {code}: {data[4:].decode(encoding='ascii')}"
            )
        elif msg_id in [
            MGMSG.MOT_MOVE_COMPLETED,
            MGMSG.MOT_MOVE_STOPPED,
            MGMSG.MOT_GET_DCSTATUSUPDATE,
        ]:
            if self.status_report_counter == 25:
                self.status_report_counter = 0
                await self.send(Message(MGMSG.MOT_ACK_DCSTATUSUPDATE))
            else:
                self.status_report_counter += 1
            # 'r' is a currently unused and reserved field
            self.position, self.velocity, r, self.status = st.unpack("<LHHL", data[2:])

    async def set_digital_outputs_config(self):
        """Set digital output pins on the motor control output port.

        Not required for the KDC101. Unimplemented.
        """
        raise NotImplementedError

    async def get_digital_outputs_config(self):
        """Get digital output pin values on the motor control output port.

        Not required for the KDC101. Unimplemented.
        """
        raise NotImplementedError

    async def set_mmi_parameters(
        self,
        mode: int,
        max_velocity: int,
        max_acceleration: int,
        direction: int,
        position1: int,
        position2: int,
        brightness: int,
        timeout: int,
        dim: int,
    ) -> None:
        """Set the operating parameters of the top panel wheel (Joystick).

        :param mode: This parameter specifies the operating mode of the
                     wheel/joy stick as follows:\n
                     * 1: Velocity Control Mode - Deflecting the wheel starts
                          a move with the velocity proportional to
                          the deflection. The maximum velocity (i.e. velocity
                          corresponding to the full deflection of the
                          joystick wheel) and acceleration are specified in the
                          max_velocity and max_acceleration parameters.
                     * 2: Jog Mode - Deflecting the wheel initiates a jog move,
                          using the parameters specified by the set_jog
                          step_size and max_velocity methods. Keeping the wheel
                          deflected repeats the move automatically after the
                          current move has completed.
                     * 3: Go To Position Mode - Deflecting the wheel starts a
                          move from the current position to one of the two
                          predefined “teach” positions. The teach positions are
                          specified in number of steps from the home position
                          in the position1 and position parameters.
        :param max_velocity: The maximum velocity of a move initiated by the
                             top panel velocity wheel.
        :param max_acceleration: The maximum acceleration of a move initiated
                                 by the top panel velocity wheel.
        :param direction: This parameter specifies the direction of a move
                          initiated by the velocity wheel as follows:\n
                          * 0: Wheel initiated moves are disabled. Wheel used
                               for menuing only.
                          * 1: Upwards rotation of the wheel results in a
                               positive motion (i.e. increased position count).
                               The following option applies only when the mode
                               is set to Velocity Control Mode (1). If set to
                               Jog Mode (2) or Go to Position Mode (3),
                               the following option is ignored.\n
                          * 2: Upwards rotation of the wheel results in a
                               negative motion (i.e. decreased position count).
        :param position1: The preset position 1 when operating in go to
                          position mode, measured in position steps from
                          the home position.
        :param position2: The preset position 2 when operating in go to
                          position mode, measured in position steps from
                          the home position.
        :param brightness: In certain applications, it may be necessary to
                           adjust the brightness of the LED display on
                           the top of the unit. The brightness is set as a
                           value from 0 (Off) to 100 (brightest). The
                           display can be turned off completely by entering a
                           setting of zero, however, pressing the
                           MENU button on the top panel will temporarily
                           illuminate the display at its lowest brightness
                           setting to allow adjustments. When the display
                           returns to its default position display mode,
                           it will turn off again.
        :param timeout: 'Burn In' of the display can occur if it remains
                        static for a long time. To prevent this, the
                        display is automatically dimmed after the time
                        interval specified in the timeout parameter has
                        elapsed. Set in minutes in the range 0 (never dimmed)
                        to 480. The dim level is set in the
                        dim parameter below.
        :param dim: The dim level, as a value from 0 (Off) to 10 (brightest)
                    but is also limited by the brightness parameter.
        """
        payload = st.pack(
            "<HHllHllHHHlHH",
            Kdc._CHANNEL,
            mode,
            max_velocity,
            max_acceleration,
            direction,
            position1,
            position2,
            brightness,
            timeout,
            dim,
            Kdc._RESERVED,
            Kdc._RESERVED,
            Kdc._RESERVED,
        )
        await self.send(Message(MGMSG.MOT_SET_KCUBEMMIPARAMS, data=payload))

    async def get_mmi_parameters(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int]:
        """Get the operating parameters of the top panel wheel (Joystick).

        :return: A 9 int tuple containing in this order: joystick mode,
                 maximum velocity, maximum acceleration, direction, position1,
                 position2, brightness, timeout, and dim. Cf.
                 :py:meth:`set_mmi_parameters() <Kdc.set_mmi_parameters>`
                 for description.
        :rtype: A 9 int tuple
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_KCUBEMMIPARAMS,
            [MGMSG.MOT_GET_KCUBEMMIPARAMS],
            Kdc._REQUEST_LENGTH,
        )
        return st.unpack("<HllHllHHH", get_msg.data[2:28])

    async def set_trigger_io_config(
        self, mode1: int, polarity1: int, mode2: int, polarity2: int
    ) -> None:
        """Set trigger intput/output parameters.

        The K-Cube motor controllers have two bidirectional trigger ports
        (TRIG1 and TRIG2) that can be used to read an external logic signal or
        output a logic level to control external equipment. Either of them can
        be independently configured as an input or an output and the active
        logic state can be selected High or Low to suit the requirements of the
        application. Electrically the ports output 5 Volt logic signals and are
        designed to be driven from a 5 Volt logic. When the port is used in the
        input mode, the logic levels are TTL compatible, i.e. a voltage level
        less than 0.8 Volt will be recognised as a logic LOW and a level
        greater than 2.4 Volt as a logic HIGH. The input contains a weak
        pull-up, so the state of the input with nothing connected will default
        to a logic HIGH. The weak pull-up feature allows a passive device, such
        as a mechanical switch to be connected directly to the input. When the
        port is used as an output it provides a push-pull drive of 5 Volts,
        with the maximum current limited to approximately 8 mA. The current
        limit prevents damage when the output is accidentally shorted to ground
        or driven to the opposite logic state by external circuity.

        **Warning**: do not drive the TRIG ports from any voltage source that
        can produce an output in excess of the normal 0 to 5 Volt logic level
        range. In any case the voltage at the TRIG ports must be limited to
        -0.25 to +5.25 Volts.

        **Input Trigger Modes**\n
        When configured as an input, the TRIG ports can be used as a general
        purpose digital input, or for triggering a relative, absolute or home
        move as follows:

        * 0x00: The trigger IO is disabled
        * 0x01: General purpose logic input (read through status bits using the
          :py:meth:`get_status_bits()
          <thorlabs_cube.driver.tcube.tdc.Tdc.get_status_bits>` method)
        * 0x02: Input trigger for relative move
        * 0x03: Input trigger for absolute move
        * 0x04: Input trigger for home move

        When used for triggering a move, the port is edge sensitive. In other
        words, it has to see a transition from the inactive to the active logic
        state (Low->High or High->Low) for the trigger input to be recognized.
        For the same reason a sustained logic level will not trigger repeated
        moves. The trigger input has to return to its inactive state first in
        order to start the next trigger.

        **Output Trigger Modes**\n
        When configured as an output, the TRIG ports can be used as a general
        purpose digital output, or to indicate motion status or to produce a
        trigger pulse at configurable positions as follows:

        * 0x0A: General purpose logic output (set using the
                :py:meth:`set_digital_outputs_config()
                <Kdc.set_digital_outputs_config>` method).
        * 0x0B: Trigger output active (level) when motor 'in motion'. The
                output trigger goes high (5V) or low (0V) (as set in the
                polarity1 and polarity2 parameters) when the stage is
                in motion.
        * 0x0C: Trigger output active (level) when motor at 'maximum velocity'.
        * 0x0D: Trigger output active (pulsed) at pre-defined positions moving
                forward (set using start_position_fwd,
                interval_fwd, num_pulses_fwd and pulse_width parameters in the
                :py:meth:`set_position_trigger_parameters()
                <Kdc.set_position_trigger_parameters>` message). Only one
                Trigger port at a time can be set to this mode.
        * 0x0E: Trigger output active (pulsed) at pre-defined positions moving
                backwards (set using start_position_rev, interval_rev,
                num_pulses_rev and pulse_width parameters in the
                :py:meth:`set_position_trigger_parameters()
                <Kdc.set_position_trigger_parameters>` message). Only one
                Trigger port at a time can be set to this mode.
        * 0x0F: Trigger output active (pulsed) at pre-defined positions moving
                forwards and backward. Only one Trigger port at a time can be
                set to this mode.

        :param mode1: TRIG1 operating mode
        :param polarity1: The active state of TRIG1 (i.e. logic high or
                          logic low)
        :param mode2: TRIG2 operating mode
        :param polarity2: The active state of TRIG2 (i.e. logic high or
                          logic low)
        """
        payload = st.pack(
            "<HHHHHQH",
            Kdc._CHANNEL,
            mode1,
            polarity1,
            mode2,
            polarity2,
            Kdc._RESERVED,
            Kdc._RESERVED,
        )
        await self.send(Message(MGMSG.MOT_SET_KCUBETRIGIOCONFIG, data=payload))

    async def get_trigger_io_config(self) -> tuple[int, int, int, int]:
        """Get trigger input/output parameters.

        :return: A 4 int tuple containing in this order: mode1, polarity1,
                 mode2, polarity2. Cf.
                 :py:meth:`get_trigger_io_config()<Kdc.get_trigger_io_config>`
                 for description.
        :rtype: A 4 int tuple
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_KCUBETRIGIOCONFIG,
            [MGMSG.MOT_GET_KCUBETRIGIOCONFIG],
            Kdc._REQUEST_LENGTH,
        )
        return st.unpack("<HHHH", get_msg.data[2:10])

    async def set_position_trigger_parameters(
        self,
        start_position_fwd: int,
        interval_fwd: int,
        num_pulses_fwd: int,
        start_position_rev: int,
        interval_rev: int,
        num_pulses_rev: int,
        pulse_width: int,
        num_cycles: int,
    ) -> None:
        """Set positioning trigger parameters.

        The K-Cube motor controllers have two bidirectional trigger ports
        (TRIG1 and TRIG2) that can be set to be used as input or output
        triggers. This method sets operating parameters used when the
        triggering mode is set to a trigger out position steps mode by calling
        the ;py:meth:`set_trigger_io_config()<Kdc.set_trigger_io_config>`
        method. As soon as position triggering is selected on either of the
        TRIG ports, the port will assert the inactive logic state. As the stage
        moves in its travel range and the actual position matches the position
        set in the start_position_fwd parameter, the TRIG port will output its
        active logic state. The active state will be output for the length of
        time specified by the pulse_width parameter, then return to its
        inactive state and schedule the next position trigger point at the
        start_position_fwd value plus the value set in the interval_fwd
        parameter. Thus when this second position is reached, the TRIG output
        will be asserted to its active state again. The sequence is repeated
        the number of times set in the num_pulses_fwd parameter. When the
        number of pulses set in the num_pulses_fwd parameter has been
        generated, the trigger engine will schedule the next position to occur
        at the position specified in the start_position_rev parameter. The same
        sequence as the forward direction is now repeated in reverse, except
        that the interval_rev and num_pulses_rev parameters apply. When the
        number of pulses has been output, the entire forward-reverse sequence
        will repeat the number of times specified by num_cycles parameter. This
        means that the total number of pulses output will be num_cycles x
        (num_pulses_fwd + num_pulses_rev).

        Once the total number of output pulses have been generated, the trigger
        output will remain inactive.

        When a unidirectional sequence is selected, only the forward or reverse
        part of the sequence will be activated.

        :param start_position_fwd: When moving forward, this is the stage
                                   position [in position counts - encoder
                                   counts or microsteps] to start the
                                   triggering sequence.
        :param interval_fwd: When moving forward, this is the interval
                             [in position counts - encoder counts or
                             microsteps] at which to output the trigger pulses.
        :param num_pulses_fwd: Number of output pulses during a forward move.
        :param start_position_rev: When moving backwards, this is the stage
                                   position [in position counts - encoder
                                   counts or microsteps] to start the
                                   triggering sequence.
        :param interval_rev: When moving backwards, this is the interval [in
                             position counts - encoder counts or microsteps] at
                             which to output the trigger pulses.
        :param num_pulses_rev: Number of output pulses during a backwards move.
        :param pulse_width: Trigger output pulse width
                            (from 1 µs to 1000000 µs).
        :param num_cycles: Number of forward/reverse move cycles.
        """
        payload = st.pack(
            "<Hllllllll",
            Kdc._CHANNEL,
            start_position_fwd,
            interval_fwd,
            num_pulses_fwd,
            start_position_rev,
            interval_rev,
            num_pulses_rev,
            pulse_width,
            num_cycles,
        )
        await self.send(
            Message(
                MGMSG.MOT_SET_KCUBEPOSTRIGPARAMS,
                data=payload,
            )
        )

    async def get_position_trigger_parameters(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int]:
        """Get the positioning trigger parameters.

        :return: An 8 int tuple containing in this order: start_position_fwd,
                 interval_fwd, num_pulses_fwd, start_position_rev,
                 interval_rev, num_pulses_rev, pulse_width, num_cycles. Cf.
                 :py:meth:`set_position_trigger_parameters()
                 <Kdc.set_position_trigger_parameters>` for description.
        :rtype: An 8 int tuple
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_KCUBEPOSTRIGPARAMS,
            [MGMSG.MOT_GET_KCUBEPOSTRIGPARAMS],
            Kdc._REQUEST_LENGTH,
        )
        return st.unpack("<llllllll", get_msg.data[2:34])


class KdcSim(TdcSim):
    def set_digital_outputs_config(self):
        raise NotImplementedError

    def get_digital_outputs_config(self):
        raise NotImplementedError

    async def set_mmi_parameters(
        self,
        mode: int,
        max_velocity: int,
        max_acceleration: int,
        direction: int,
        position1: int,
        position2: int,
        brightness: int,
        timeout: int,
        dim: int,
    ) -> None:
        self.mode = mode
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.direction = direction
        self.position1 = position1
        self.position2 = position2
        self.brightness = brightness
        self.timeout = timeout
        self.dim = dim

    async def get_mmi_parameters(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int]:
        return (
            self.mode,
            self.max_velocity,
            self.max_acceleration,
            self.direction,
            self.position1,
            self.position2,
            self.brightness,
            self.timeout,
            self.dim,
        )

    async def set_trigger_io_config(
        self, mode1: int, polarity1: int, mode2: int, polarity2: int
    ) -> None:
        self.mode1 = mode1
        self.polarity1 = polarity1
        self.mode2 = mode2
        self.polarity2 = polarity2

    async def get_trigger_io_config(self) -> tuple[int, int, int, int]:
        return (self.mode1, self.polarity1, self.mode2, self.polarity2)

    async def set_position_trigger_parameters(
        self,
        start_position_fwd: int,
        interval_fwd: int,
        num_pulses_fwd: int,
        start_position_rev: int,
        interval_rev: int,
        num_pulses_rev: int,
        pulse_width: int,
        num_cycles: int,
    ) -> None:
        self.start_position_fwd = start_position_fwd
        self.interval_fwd = interval_fwd
        self.num_pulses_fwd = num_pulses_fwd
        self.start_position_rev = start_position_rev
        self.interval_rev = interval_rev
        self.num_pulses_rev = num_pulses_rev
        self.pulse_width = pulse_width
        self.num_cycles = num_cycles

    async def get_position_trigger_parameters(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int]:
        return (
            self.start_position_fwd,
            self.interval_fwd,
            self.num_pulses_fwd,
            self.start_position_rev,
            self.interval_rev,
            self.num_pulses_rev,
            self.pulse_width,
            self.num_cycles,
        )
