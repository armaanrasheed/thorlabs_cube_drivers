import struct as st

from thorlabs_cube.driver.base import _Cube
from thorlabs_cube.driver.message import MGMSG, Message, MsgError


class Tdc(_Cube):
    """TDC001 T-Cube Motor Controller class"""

    def __init__(self, serial_dev: str):
        super().__init__(serial_dev)
        self.status_report_counter = 0

    async def handle_message(self, msg):
        msg_id = msg.id
        data = msg.data

        if msg_id == MGMSG.HW_DISCONNECT:
            raise MsgError("Error: Please disconnect the TDC001")
        elif msg_id == MGMSG.HW_RESPONSE:
            raise MsgError(
                "Hardware error, please disconnect " "and reconnect the TDC001"
            )
        elif msg_id == MGMSG.HW_RICHRESPONSE:
            (code,) = st.unpack("<H", data[2:4])
            raise MsgError(
                "Hardware error {}: {}".format(code, data[4:].decode(encoding="ascii"))
            )
        elif (
            msg_id == MGMSG.MOT_MOVE_COMPLETED
            or msg_id == MGMSG.MOT_MOVE_STOPPED
            or msg_id == MGMSG.MOT_GET_DCSTATUSUPDATE
        ):
            if self.status_report_counter == 25:
                self.status_report_counter = 0
                await self.send(Message(MGMSG.MOT_ACK_DCSTATUSUPDATE))
            else:
                self.status_report_counter += 1
            # 'r' is a currently unused and reserved field
            self.position, self.velocity, r, self.status = st.unpack(
                "<LHHL",
                data[2:],
            )

    async def is_moving(self):
        status_bits = await self.get_status_bits()
        return (status_bits & 0x2F0) != 0

    async def set_pot_parameters(
        self, zero_wnd, vel1, wnd1, vel2, wnd2, vel3, wnd3, vel4
    ):
        """Set pot parameters.

        :param zero_wnd: The deflection from the mid position (in ADC counts
            0 to 127) before motion can start.
        :param vel1: The velocity to move when between zero_wnd and wnd1.
        :param wnd1: The deflection from the mid position (in ADC counts
            zero_wnd to 127) to apply vel1.
        :param vel2: The velocity to move when between wnd1 and wnd2.
        :param wnd2: The deflection from the mid position (in ADC counts
            wnd1 to 127) to apply vel2.
        :param vel3: The velocity to move when between wnd2 and wnd3.
        :param wnd3: The deflection from the mid position (in ADC counts
            wnd2 to 127) to apply vel3.
        :param vel4: The velocity to move when beyond wnd3.
        """
        payload = st.pack(
            "<HHLHLHLHL", 1, zero_wnd, vel1, wnd1, vel2, wnd2, vel3, wnd3, vel4
        )
        await self.send(Message(MGMSG.MOT_SET_POTPARAMS, data=payload))

    async def get_pot_parameters(self):
        """Get pot parameters.

        :return: An 8 int tuple containing the following values: zero_wnd,
            vel1, wnd1, vel2, wnd2, vel3, wnd3, vel4. See
            :py:meth:`set_pot_parameters()<Tdc.set_pot_parameters>` for a
            description of each tuple element meaning.
        :rtype: An 8 int tuple
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_POTPARAMS, [MGMSG.MOT_GET_POTPARAMS], 1
        )
        return st.unpack("<HLHLHLHL", get_msg.data[2:])

    async def hub_get_bay_used(self):
        get_msg = await self.send_request(
            MGMSG.HUB_REQ_BAYUSED, [MGMSG.HUB_GET_BAYUSED]
        )
        return get_msg.param1

    async def set_position_counter(self, position):
        """Set the "live" position count in the controller.

        In general, this command is not normally used. Instead, the stage is
        homed immediately after power-up; and after the homing process is
        completed, the position counter is automatically updated to show the
        actual position.

        :param position: The new value of the position counter.
        """
        payload = st.pack("<Hl", 1, position)
        await self.send(Message(MGMSG.MOT_SET_POSCOUNTER, data=payload))

    async def get_position_counter(self):
        """Get the "live" position count from the controller.

        :return: The value of the position counter.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_POSCOUNTER, [MGMSG.MOT_GET_POSCOUNTER], 1
        )
        return st.unpack("<l", get_msg.data[2:])[0]

    async def set_encoder_counter(self, encoder_count):
        """Set encoder count in the controller.

        This is only applicable to stages and actuators fitted
        with an encoder. In general this command is not normally used.
        Instead the device is homed at power-up.

        :param encoder_count: The new value of the encoder counter.
        """
        payload = st.pack("<Hl", 1, encoder_count)
        await self.send(Message(MGMSG.MOT_SET_ENCCOUNTER, data=payload))

    async def get_encoder_counter(self):
        """Get encoder count from the controller.

        :return: The value of the encoder counter.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_ENCCOUNTER, [MGMSG.MOT_GET_ENCCOUNTER], 1
        )
        return st.unpack("<l", get_msg.data[2:])[0]

    async def set_velocity_parameters(self, acceleration, max_velocity):
        """Set the trapezoidal velocity parameter.

        :param acceleration: The acceleration in encoder counts/sec/sec.
        :param max_velocity: The maximum (final) velocity in counts/sec.
        """
        payload = st.pack("<HLLL", 1, 0, acceleration, max_velocity)
        await self.send(Message(MGMSG.MOT_SET_VELPARAMS, data=payload))

    async def get_velocity_parameters(self):
        """Get the trapezoidal velocity parameters.

        :return: A 2 int tuple: (acceleration, max_velocity).
        :rtype: A 2 int tuple (int, int)
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_VELPARAMS, [MGMSG.MOT_GET_VELPARAMS], 1
        )
        return st.unpack("<LL", get_msg.data[6:])

    async def set_jog_parameters(
        self, mode, step_size, acceleration, max_velocity, stop_mode
    ):
        """Set the velocity jog parameters.

        :param mode: 1 for continuous jogging, 2 for single step jogging.
        :param step_size: The jog step size in encoder counts.
        :param acceleration: The acceleration in encoder counts/sec/sec.
        :param max_velocity: The maximum (final) velocity in encoder
            counts/sec.
        :param stop_mode: 1 for immediate (abrupt) stop, 2 for profiled stop
            (with controlled deceleration).
        """
        payload = st.pack(
            "<HHLLLLH",
            1,
            mode,
            step_size,
            0,
            acceleration,
            max_velocity,
            stop_mode,
        )
        await self.send(Message(MGMSG.MOT_SET_JOGPARAMS, data=payload))

    async def get_jog_parameters(self):
        """Get the velocity jog parameters.

        :return: A 5 int tuple containing in this order: jog_mode,
            step_size, acceleration, max_velocity, stop_mode
        :rtype: A 5 int tuple.
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_JOGPARAMS, [MGMSG.MOT_GET_JOGPARAMS], 1
        )
        (jog_mode, step_size, _, acceleration, max_velocity, stop_mode) = st.unpack(
            "<HLLLLH", get_msg.data[2:]
        )
        return jog_mode, step_size, acceleration, max_velocity, stop_mode

    async def set_gen_move_parameters(self, backlash_distance):
        """Set the backlash distance.

        :param backlash_distance: The value of the backlash distance,
            which specifies the relative distance in position counts.
        """
        payload = st.pack("<Hl", 1, backlash_distance)
        await self.send(Message(MGMSG.MOT_SET_GENMOVEPARAMS, data=payload))

    async def get_gen_move_parameters(self):
        """Get the backlash distance.

        :return: The value of the backlash distance.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_GENMOVEPARAMS, [MGMSG.MOT_GET_GENMOVEPARAMS], 1
        )
        return st.unpack("<l", get_msg.data[2:])[0]

    async def set_move_relative_parameters(self, relative_distance):
        """Set the following relative move parameter: relative_distance.

        :param relative_distance: The distance to move. This is a signed
            integer that specifies the relative distance in position encoder
            counts.
        """
        payload = st.pack("<Hl", 1, relative_distance)
        await self.send(Message(MGMSG.MOT_SET_MOVERELPARAMS, data=payload))

    async def get_move_relative_parameters(self):
        """Get the relative distance move parameter.

        :return: The relative distance move parameter.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_MOVERELPARAMS, [MGMSG.MOT_GET_MOVERELPARAMS], 1
        )
        return st.unpack("<l", get_msg.data[2:])[0]

    async def set_move_absolute_parameters(self, absolute_position):
        """Set the following absolute move parameter: absolute_position.

        :param absolute_position: The absolute position to move. This is a
            signed integer that specifies the absolute move position in encoder
            counts.
        """
        payload = st.pack("<Hl", 1, absolute_position)
        await self.send(Message(MGMSG.MOT_SET_MOVEABSPARAMS, data=payload))

    async def get_move_absolute_parameters(self):
        """Get the absolute position move parameter.

        :return: The absolute position to move.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_MOVEABSPARAMS, [MGMSG.MOT_GET_MOVEABSPARAMS], 1
        )
        return st.unpack("<l", get_msg.data[2:])[0]

    async def set_home_parameters(self, home_velocity):
        """Set the homing velocity parameter.

        :param home_velocity: Homing velocity.
        """
        payload = st.pack("<HHHLL", 1, 0, 0, home_velocity, 0)
        await self.send(Message(MGMSG.MOT_SET_HOMEPARAMS, data=payload))

    async def get_home_parameters(self):
        """Get the homing velocity parameter.

        :return: The homing velocity.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_HOMEPARAMS, [MGMSG.MOT_GET_HOMEPARAMS], 1
        )
        return st.unpack("<L", get_msg.data[6:10])[0]

    async def move_home(self):
        """Start a home move sequence.

        This call is blocking until device is homed or move is stopped.
        """
        await self.send_request(
            MGMSG.MOT_MOVE_HOME,
            [MGMSG.MOT_MOVE_HOMED, MGMSG.MOT_MOVE_STOPPED],
            1,
        )

    async def set_limit_switch_parameters(
        self,
        cw_hw_limit,
        ccw_hw_limit,
        cw_sw_limit=0,
        ccw_sw_limit=0,
        sw_limit_mode=0x1,
    ):
        """Set the limit switch parameters.

        :param cw_hw_limit: The operation of clockwise hardware limit switch
            when contact is made.

            0x01 Ignore switch or switch not present.

            0x02 Switch makes on contact.

            0x03 Switch breaks on contact.

            0x04 Switch makes on contact - only used for homes (e.g. limit
            switched rotation stages).

            0x05 Switch breaks on contact - only used for homes (e.g. limit
            switched rotations stages).

            0x06 For PMD based brushless servo controllers only - uses index
            mark for homing.

            Note. Set upper bit to swap CW and CCW limit switches in code. Both
            CWHardLimit and CCWHardLimit structure members will have the upper
            bit set when limit switches have been physically swapped.
        :param ccw_hw_limit: The operation of counter clockwise hardware limit
            switch when contact is made.
        :param cw_sw_limit: Clockwise software limit in position steps, as a
            32 bit unsigned long. (Not applicable to TDC001 units)
        :param ccw_sw_limit: Counter clockwise software limit in position steps
            (scaling as for CW limit). (Not applicable to TDC001 units)
        :param sw_limit_mode: Software limit switch mode

            0x01 Ignore Limit

            0x02 Stop Immediate at Limit

            0x03 Profiled Stop at limit

            0x80 Rotation Stage Limit (bitwise OR'd with one of the settings
            above) (Not applicable to TDC001 units)
        """
        payload = st.pack(
            "<HHHLLH",
            1,
            cw_hw_limit,
            ccw_hw_limit,
            cw_sw_limit,
            ccw_sw_limit,
            sw_limit_mode,
        )
        await self.send(Message(MGMSG.MOT_SET_LIMSWITCHPARAMS, data=payload))

    async def get_limit_switch_parameters(self):
        """Get the limit switch parameters.

        :return: A 5 int tuple containing the following in order: cw_hw_limit,
         ccw_hw_limit, cw_sw_limit, ccw_sw_limit, sw_limit_mode. Cf.
         description in
         :py:meth:`set_limit_switch_parameters()
         <Tdc.set_limit_switch_parameters>`
         method.
        :rtype: A 5 int tuple.
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_LIMSWITCHPARAMS, [MGMSG.MOT_GET_LIMSWITCHPARAMS], 1
        )
        return st.unpack("<HHLLH", get_msg.data[2:])

    async def move_relative_memory(self):
        """Start a relative move of distance in the controller's memory

        The relative distance parameter used for the move will be the parameter
        sent previously by a :py:meth:`set_move_relative_parameters()
        <Tdc.set_move_relative_parameters>`
        command.
        """
        await self.send_request(
            MGMSG.MOT_MOVE_RELATIVE,
            [MGMSG.MOT_MOVE_COMPLETED, MGMSG.MOT_MOVE_STOPPED],
            1,
        )

    async def move_relative(self, relative_distance):
        """Start a relative move

        :param relative_distance: The distance to move in position encoder
            counts.
        """
        payload = st.pack("<Hl", 1, relative_distance)
        await self.send_request(
            MGMSG.MOT_MOVE_RELATIVE,
            [MGMSG.MOT_MOVE_COMPLETED, MGMSG.MOT_MOVE_STOPPED],
            data=payload,
        )

    async def move_absolute_memory(self):
        """Start an absolute move of distance in the controller's memory.

        The absolute move position parameter used for the move will be the
        parameter sent previously by a :py:meth:`set_move_absolute_parameters()
        <Tdc.set_move_absolute_parameters>`
        command.
        """
        await self.send_request(
            MGMSG.MOT_MOVE_ABSOLUTE,
            [MGMSG.MOT_MOVE_COMPLETED, MGMSG.MOT_MOVE_STOPPED],
            param1=1,
        )

    async def move_absolute(self, absolute_distance):
        """Start an absolute move.

        :param absolute_distance: The distance to move. This is a signed
            integer that specifies the absolute distance in position encoder
            counts.
        """
        payload = st.pack("<Hl", 1, absolute_distance)
        await self.send_request(
            MGMSG.MOT_MOVE_ABSOLUTE,
            [MGMSG.MOT_MOVE_COMPLETED, MGMSG.MOT_MOVE_STOPPED],
            data=payload,
        )

    async def move_jog(self, direction):
        """Start a jog move.

        :param direction: The direction to jog. 1 is forward, 2 is backward.
        """
        await self.send_request(
            MGMSG.MOT_MOVE_JOG,
            [MGMSG.MOT_MOVE_COMPLETED, MGMSG.MOT_MOVE_STOPPED],
            param1=1,
            param2=direction,
        )

    async def move_velocity(self, direction):
        """Start a move.

        When this method is called, the motor will move continuously in the
        specified direction using the velocity parameter set by the
        :py:meth:`set_move_relative_parameters()
        <Tdc.set_move_relative_parameters>`
        command until a :py:meth:`move_stop()<Tdc.move_stop>` command (either
        StopImmediate or StopProfiled) is called, or a limit switch is reached.

        :param direction: The direction to jog: 1 to move forward, 2 to move
            backward.
        """
        await self.send(Message(MGMSG.MOT_MOVE_VELOCITY, param1=1, param2=direction))

    async def move_stop(self, stop_mode):
        """Stop any type of motor move.

        Stops any of those motor move: relative, absolute, homing or move at
        velocity.

        :param stop_mode: The stop mode defines either an immediate (abrupt)
            or profiled stop. Set this byte to 1 to stop immediately, or to 2
            to stop in a controlled (profiled) manner.
        """
        if await self.is_moving():
            await self.send_request(
                MGMSG.MOT_MOVE_STOP,
                [MGMSG.MOT_MOVE_STOPPED, MGMSG.MOT_MOVE_COMPLETED],
                1,
                stop_mode,
            )

    async def set_dc_pid_parameters(
        self,
        proportional,
        integral,
        differential,
        integral_limit,
        filter_control=0x0F,
    ):
        """Set the position control loop parameters.

        :param proportional: The proportional gain, values in range [0; 32767].
        :param integral: The integral gain, values in range [0; 32767].
        :param differential: The differential gain, values in range [0; 32767].
        :param integral_limit: The integral limit parameter is used to cap the
            value of the integrator to prevent runaway of the integral sum at
            the output. Values are in range [0; 32767]. If set to 0, then
            integration term in the PID loop is ignored.
        :param filter_control: Identifies which of the above are applied by
            setting the corresponding bit to 1. By default, all parameters are
            applied, and this parameter is set to 0x0F (1111).
        """
        payload = st.pack(
            "<HLLLLH",
            1,
            proportional,
            integral,
            differential,
            integral_limit,
            filter_control,
        )
        await self.send(Message(MGMSG.MOT_SET_DCPIDPARAMS, data=payload))

    async def get_dc_pid_parameters(self):
        """Get the position control loop parameters.

        :return: A 5 int tuple containing in this order:
            proportional gain, integral gain, differential gain, integral limit
            and filter control. Cf. :py:meth:`set_dc_pid_parameters()
            <Tdc.set_dc_pid_parameters>`
            for precise description.
        :rtype: A 5 int tuple.
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_DCPIDPARAMS, [MGMSG.MOT_GET_DCPIDPARAMS], 1
        )
        return st.unpack("<LLLLH", get_msg.data[2:])

    async def set_av_modes(self, mode_bits):
        """Set the LED indicator modes.

        The LED on the control keyboard can be configured to indicate certain
        driver states.

        :param mode_bits: Set the bit 0 will make the LED flash when the
            'Ident' message is sent.
            Set the bit 1 will make the LED flash when the motor reaches a
            forward or reverse limit switch.
            Set the bit 3 (value 8) will make the LED lit when motor is moving.
        """
        payload = st.pack("<HH", 1, mode_bits)
        await self.send(Message(MGMSG.MOT_SET_AVMODES, data=payload))

    async def get_av_modes(self):
        """Get the LED indicator mode bits.

        :return: The LED indicator mode bits.
        :rtype: int
        """
        get_msg = self.send_request(
            MGMSG.MOT_REQ_AVMODES,
            [MGMSG.MOT_GET_AVMODES],
            1,
        )
        return st.unpack("<H", get_msg.data[2:])[0]

    async def set_button_parameters(self, mode, position1, position2):
        """Set button parameters.

        The control keypad can be used either to jog the motor, or to perform
        moves to absolute positions. This function is used to set the front
        panel button functionality.

        :param mode: If set to 1, the buttons are used to jog the motor. Once
            set to this mode, the move parameters for the buttons are taken
            from the arguments of the :py:meth:`set_jog_parameters()
            <Tdc.set_jog_parameters>`
            method. If set to 2, each button can be programmed with a
            differente position value such that the controller will move the
            motor to that position when the specific button is pressed.
        :param position1: The position (in encoder counts) to which the motor
            will move when the top button is pressed.
        :param position2: The position (in encoder counts) to which the motor
            will move when the bottom button is pressed.
        """
        payload = st.pack("<HHllHH", 1, mode, position1, position2, 0, 0)
        await self.send(Message(MGMSG.MOT_SET_BUTTONPARAMS, data=payload))

    async def get_button_parameters(self):
        """Get button parameters.

        :return: A 3 int tuple containing in this order: button mode,
            position1 and position2. Cf. :py:meth:`set_button_parameters()
            <Tdc.set_button_parameters>`
            for description.
        :rtype: A 3 int tuple
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_BUTTONPARAMS, [MGMSG.MOT_GET_BUTTONPARAMS], 1
        )
        return st.unpack("<Hll", get_msg.data[2:12])

    async def set_eeprom_parameters(self, msg_id):
        """Save the parameter settings for the specified message.

        :param msg_id: The message ID of the message containing the parameters
            to be saved.
        """
        payload = st.pack("<HH", 1, msg_id)
        await self.send(Message(MGMSG.MOT_SET_EEPROMPARAMS, data=payload))

    async def get_dc_status_update(self):
        """Request a status update from the motor.

        This can be used instead of enabling regular updates.

        :return: A 3 int tuple containing in this order: position,
            velocity, status bits.
        :rtype: A 3 int tuple
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_DCSTATUSUPDATE, [MGMSG.MOT_GET_DCSTATUSUPDATE], 1
        )
        pos, vel, _, stat = st.unpack("<LHHL", get_msg.data[2:])
        return pos, vel, stat

    async def get_status_bits(self):
        """Request a cut down version of the status update with status bits.

        :return: The motor status.
        :rtype:
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_STATUSBITS, [MGMSG.MOT_GET_STATUSBITS], 1
        )
        return st.unpack("<L", get_msg.data[2:])[0]

    async def suspend_end_of_move_messages(self):
        """Disable all unsolicited "end of move" messages and error messages
        returned by the controller.

        i.e., MGMSG.MOT_MOVE_STOPPED, MGMSG.MOT_MOVE_COMPLETED,
        MGMSGS_MOT_MOVE_HOMED
        """
        await self.send(Message(MGMSG.MOT_SUSPEND_ENDOFMOVEMSGS))

    async def resume_end_of_move_messages(self):
        """Resume all unsolicited "end of move" messages and error messages
        returned by the controller.

        i.e., MGMSG.MOT_MOVE_STOPPED, MGMSG.MOT_MOVE_COMPLETED,
        MGMSG.MOT_MOVE_HOMED

        The command also disables the error messages that the controller sends
        when an error condition is detected:
        MGMSG.HW_RESPONSE,
        MGMSG.HW_RICHRESPONSE
        """
        await self.send(Message(MGMSG.MOT_RESUME_ENDOFMOVEMSGS))


class TdcSim:
    def close(self):
        pass

    def module_identify(self):
        pass

    def set_pot_parameters(
        self,
        zero_wnd,
        vel1,
        wnd1,
        vel2,
        wnd2,
        vel3,
        wnd3,
        vel4,
    ):
        self.zero_wnd = zero_wnd
        self.vel1 = vel1
        self.wnd1 = wnd1
        self.vel2 = vel2
        self.wnd2 = wnd2
        self.vel3 = vel3
        self.wnd3 = wnd3
        self.vel4 = vel4

    def get_pot_parameters(self):
        return (
            self.zero_wnd,
            self.vel1,
            self.wnd1,
            self.vel2,
            self.wnd2,
            self.vel3,
            self.wnd3,
            self.vel4,
        )

    def hub_get_bay_used(self):
        return False

    def set_position_counter(self, position):
        self.position = position

    def get_position_counter(self):
        return self.position

    def set_encoder_counter(self, encoder_count):
        self.encoder_count = encoder_count

    def get_encoder_counter(self):
        return self.encoder_count

    def set_velocity_parameters(self, acceleration, max_velocity):
        self.acceleration = acceleration
        self.max_velocity = max_velocity

    def get_velocity_parameters(self):
        return self.acceleration, self.max_velocity

    def set_jog_parameters(
        self, mode, step_size, acceleration, max_velocity, stop_mode
    ):
        self.jog_mode = mode
        self.step_size = step_size
        self.acceleration = acceleration
        self.max_velocity = max_velocity
        self.stop_mode = stop_mode

    def get_jog_parameters(self):
        return (
            self.jog_mode,
            self.step_size,
            self.acceleration,
            self.max_velocity,
            self.stop_mode,
        )

    def set_gen_move_parameters(self, backlash_distance):
        self.backlash_distance = backlash_distance

    def get_gen_move_parameters(self):
        return self.backlash_distance

    def set_move_relative_parameters(self, relative_distance):
        self.relative_distance = relative_distance

    def get_move_relative_parameters(self):
        return self.relative_distance

    def set_move_absolute_parameters(self, absolute_position):
        self.absolute_position = absolute_position

    def get_move_absolute_parameters(self):
        return self.absolute_position

    def set_home_parameters(self, home_velocity):
        self.home_velocity = home_velocity

    def get_home_parameters(self):
        return self.home_velocity

    def move_home(self):
        pass

    def set_limit_switch_parameters(
        self,
        cw_hw_limit,
        ccw_hw_limit,
        cw_sw_limit=0,
        ccw_sw_limit=0,
        sw_limit_mode=0x1,
    ):
        self.cw_hw_limit = cw_hw_limit
        self.ccw_hw_limit = ccw_hw_limit
        self.cw_sw_limit = cw_sw_limit
        self.ccw_sw_limit = ccw_sw_limit
        self.sw_limit_mode = sw_limit_mode

    def get_limit_switch_parameters(self):
        return (
            self.cw_hw_limit,
            self.ccw_hw_limit,
            self.cw_sw_limit,
            self.ccw_sw_limit,
            self.sw_limit_mode,
        )

    def move_relative_memory(self):
        pass

    def move_relative(self, relative_distance):
        pass

    def move_absolute_memory(self):
        pass

    def move_absolute(self, absolute_distance):
        pass

    def move_jog(self, direction):
        pass

    def move_velocity(self, direction):
        pass

    def move_stop(self, stop_mode):
        pass

    def set_dc_pid_parameters(
        self,
        proportional,
        integral,
        differential,
        integral_limit,
        filter_control=0x0F,
    ):
        self.proportional = proportional
        self.integral = integral
        self.differential = differential
        self.integral_limit = integral_limit
        self.filter_control = filter_control

    def get_dc_pid_parameters(self):
        return (
            self.proportional,
            self.integral,
            self.differential,
            self.integral_limit,
            self.filter_control,
        )

    def set_av_modes(self, mode_bits):
        self.mode_bits = mode_bits

    def get_av_modes(self):
        return self.mode_bits

    def set_button_parameters(self, mode, position1, position2):
        self.mode = mode
        self.position1 = position1
        self.position2 = position2

    def get_button_parameters(self):
        return self.mode, self.position1, self.position2

    def set_eeprom_parameters(self, msg_id):
        pass

    def get_dc_status_update(self):
        return 0, 0, 0x80000400  # FIXME: not implemented yet for simulation

    def get_status_bits(self):
        return 0x80000400  # FIXME: not implemented yet for simulation

    def suspend_end_of_move_messages(self):
        pass

    def resume_end_of_move_messages(self):
        pass
