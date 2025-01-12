import struct as st
from typing import Optional

from thorlabs_cube.driver.base import _Cube
from thorlabs_cube.driver.message import MGMSG, Message, MsgError


class Tpz(_Cube):
    """Either :py:meth:`set_tpz_io_settings()<Tpz.set_tpz_io_settings>`
    or :py:meth:`get_tpz_io_settings()<Tpz.get_tpz_io_settings>` must
    be completed to finish initialising the driver.
    """

    def __init__(self, serial_dev) -> None:
        super().__init__(serial_dev)
        self.voltage_limit: Optional[int] = None

    async def handle_message(self, msg) -> None:
        msg_id = msg.id
        data = msg.data

        if msg_id == MGMSG.HW_DISCONNECT:
            raise MsgError("Error: Please disconnect the TPZ001")
        elif msg_id == MGMSG.HW_RESPONSE:
            raise MsgError(
                "Hardware error, please disconnect " "and reconnect the TPZ001"
            )
        elif msg_id == MGMSG.HW_RICHRESPONSE:
            (code,) = st.unpack("<H", data[2:4])
            raise MsgError(
                "Hardware error {}: {}".format(
                    code,
                    data[4:].decode(encoding="ascii"),
                )
            )

    async def set_position_control_mode(self, control_mode: int) -> None:
        """Set the control loop mode.

        When in closed-loop mode, position is maintained by a feedback signal
        from the piezo actuator. This is only possible when using actuators
        equipped with position sensing.

        :param control_mode: 0x01 for Open Loop (no feedback).
            0x02 for Closed Loop (feedback employed).
            0x03 for Open Loop Smooth.
            0x04 for Closed Loop Smooth.
        """
        await self.send(
            Message(
                MGMSG.PZ_SET_POSCONTROLMODE, param1=Tpz._CHANNEL, param2=control_mode
            )
        )

    async def get_position_control_mode(self) -> int:
        """Get the control loop mode.

        :return: Returns the control mode.
            0x01 for Open Loop (no feedback).
            0x02 for Closed Loop (feedback employed).
            0x03 for Open Loop Smooth.
            0x04 for Closed Loop Smooth.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_POSCONTROLMODE, [MGMSG.PZ_GET_POSCONTROLMODE], Tpz._CHANNEL
        )
        return get_msg.param2

    async def set_output_volts(self, voltage: float) -> None:
        """Set output voltage applied to the piezo actuator.

        This command is only applicable in Open Loop mode. If called when in
        Closed Loop mode it is ignored.

        :param voltage: The output voltage applied to the piezo when operating
            in open loop mode. The voltage value must be in range
            [0; voltage_limit]. Voltage_limit being set by the
            :py:meth:`set_tpz_io_settings()<Tpz.set_tpz_io_settings>`
            method between the three values 75 V, 100 V and 150 V.
        """
        if self.voltage_limit is None:
            raise ValueError("Voltage limit is not set")

        if voltage < 0 or voltage > self.voltage_limit:
            raise ValueError(
                "Voltage must be in range [0;{}]".format(self.voltage_limit)
            )
        volt = int(voltage * 32767 / self.voltage_limit)
        payload = st.pack("<HH", Tpz._CHANNEL, volt)
        await self.send(Message(MGMSG.PZ_SET_OUTPUTVOLTS, data=payload))

    async def get_output_volts(self) -> float:
        """Get the output voltage applied to the piezo actuator.

        :return: The output voltage.
        :rtype: float
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_OUTPUTVOLTS, [MGMSG.PZ_GET_OUTPUTVOLTS], Tpz._CHANNEL
        )
        return st.unpack("<H", get_msg.data[2:])[0] * self.voltage_limit / 32767

    async def set_output_position(self, position_sw: int) -> None:
        """Set output position of the piezo actuator.

        This command is only applicable in Closed Loop mode. If called when in
        Open Loop mode, it is ignored. The position of the actuator is relative
        to the datum set for the arrangement using the ZeroPosition method.

        :param position_sw: The output position of the piezo relative to the
            zero position. The voltage is set in the range [0; 32767] or
            [0; 65535] depending on the unit. This corresponds to 0 to 100% of
            the maximum piezo extension.
        """
        payload = st.pack("<HH", Tpz._CHANNEL, position_sw)
        await self.send(Message(MGMSG.PZ_SET_OUTPUTPOS, data=payload))

    async def get_output_position(self) -> int:
        """Get output position of piezo actuator.

        :return: The output position of the piezo relative to the zero
            position.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_OUTPUTPOS, [MGMSG.PZ_GET_OUTPUTPOS], Tpz._CHANNEL
        )
        return st.unpack("<H", get_msg.data[2:])[0]

    async def set_input_volts_source(self, volt_src: int) -> None:
        """Set the input source(s) which controls the output from the HV
        amplifier circuit (i.e. the drive to the piezo actuators).

        :param volt_src: The following values are entered into the VoltSrc
            parameter to select the various analog sources:

            0x00 Software Only: Unit responds only to software inputs and the
            HV amp output is that set using the :py:meth:`set_output_volts()`
            <Tpz.set_output_volts>` method.

            0x01 External Signal: Unit sums the differential signal on the rear
            panel EXT IN(+) and EXT IN(-) connectors with the voltage set
            using the set_outputvolts method.

            0x02 Potentiometer: The HV amp output is controlled by a
            potentiometer input (either on the control panel, or connected
            to the rear panel User I/O D-type connector) summed with the
            voltage set using the set_outputvolts method.

            The values can be bitwise or'ed to sum the software source with
            either or both of the other source options.
        """
        payload = st.pack("<HH", Tpz._CHANNEL, volt_src)
        await self.send(Message(MGMSG.PZ_SET_INPUTVOLTSSRC, data=payload))

    async def get_input_volts_source(self) -> int:
        """Get the input source(s) which controls the output from the HV
        amplifier circuit.

        :return: Value which selects the various analog sources, cf.
            :py:meth:`set_input_volts_source()<Tpz.set_input_volts_source>`
            method docstring for meaning of bits.
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_INPUTVOLTSSRC, [MGMSG.PZ_GET_INPUTVOLTSSRC], Tpz._CHANNEL
        )
        return st.unpack("<H", get_msg.data[2:])[0]

    async def set_pi_constants(self, prop_const: int, int_const: int) -> None:
        """Set the proportional and integration feedback loop constants.

        These parameters determine the response characteristics when operating
        in closed loop mode.
        The processors within the controller compare the required (demanded)
        position with the actual position to create an error, which is then
        passed through a digital PI-type filter. The filtered value is used to
        develop an output voltage to drive the pizeo.

        :param prop_const: Value of the proportional term in range [0; 255].
        :param int_const: Value of the integral term in range [0; 255].
        """
        payload = st.pack("<HHH", Tpz._CHANNEL, prop_const, int_const)
        await self.send(Message(MGMSG.PZ_SET_PICONSTS, data=payload))

    async def get_pi_constants(self) -> tuple[int, int]:
        """Get the proportional and integration feedback loop constants.

        :return: Returns a tuple whose first element is the proportional
            term and the second element is the integral term.
        :rtype: a 2 int elements tuple : (int, int)
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_PICONSTS, [MGMSG.PZ_GET_PICONSTS], Tpz._CHANNEL
        )
        return st.unpack("<HH", get_msg.data[2:])

    async def set_output_lut(self, lut_index: int, output: float) -> None:
        """Set the ouput LUT values for WGM (Waveform Generator Mode).

        It is possible to use the controller in an arbitrary Waveform
        Generator Mode (WGM). Rather than the unit outputting an adjustable
        but static voltage or position, the WGM allows the user to define a
        voltage or position sequence to be output, either periodically or a
        fixed number of times, with a selectable interval between adjacent
        samples.

        This waveform generation function is particularly useful for
        operations such as scanning over a particular area, or in any other
        application that requires a predefined movement sequence. The waveform
        is stored as values in an array, with a maximum of 513 samples.

        The samples can have the meaning of voltage or position; if
        open loop operation is specified when the samples are output, then
        their meaning is voltage and vice versa, if the channel is set to
        closed loop operation, the samples are interpreted as position values.

        If the waveform to be output requires less than 513 samples, it is
        sufficient to download the desired number of samples. This function is
        used to load the LUT array with the required output waveform. The
        applicable channel is specified by the Chan Ident parameter If only a
        sub set of the array is being used (as specified by the cyclelength
        parameter of the :py:meth:`set_output_lut_parameters()`
        <Tpz.set_output_lut_parameters>`
        function), then only the first cyclelength values need to be set. In
        this manner, any arbitrary voltage waveform can be programmed into the
        LUT. Note. The LUT values are output by the system at a maximum
        bandwidth of 7 KHz, e.g. 500 LUT values will take approximately 71 ms
        to be clocked out.

        :param lut_index: The position in the array of the value to be set (0
            to 512 for TPZ).
        :param output: The voltage value to be set. Values are in the range
            [0; voltage_limit]. Voltage_limit being set with the
            :py:meth:`set_tpz_io_settings<Tpz.set_tpz_io_settings>`
            method.
        """
        if self.voltage_limit is None:
            raise ValueError("Voltage limit is not set")

        volt = round(output * 32767 / self.voltage_limit)
        payload = st.pack("<HHH", Tpz._CHANNEL, lut_index, volt)
        await self.send(Message(MGMSG.PZ_SET_OUTPUTLUT, data=payload))

    async def get_output_lut(self) -> tuple[int, float]:
        """Get the ouput LUT values for WGM (Waveform Generator Mode).

        :return: a tuple whose first element is the lut index and the second is
            the voltage output value.
        :rtype: a 2 elements tuple (int, float)
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_OUTPUTLUT, [MGMSG.PZ_GET_OUTPUTLUT], Tpz._CHANNEL
        )
        index, output = st.unpack("<Hh", get_msg.data[2:])
        return index, output * self.voltage_limit / 32767

    async def set_output_lut_parameters(
        self,
        mode: int,
        cycle_length: int,
        num_cycles: int,
        delay_time: int,
        precycle_rest: int,
        postcycle_rest: int,
    ) -> None:
        """Set Waveform Generator Mode parameters.

        It is possible to use the controller in an arbitrary Waveform
        Generator Mode (WGM). Rather than the unit outputting an adjustable
        but static voltage or position, the WGM allows the user to define a
        voltage or position sequence to be output, either periodically or a
        fixed number of times, with a selectable interval between adjacent
        samples.
        This waveform generation function is particularly useful for operations
        such as scanning over a particular area, or in any other application
        that requires a predefined movement sequence. This function is used to
        set parameters which control the output of the LUT array.

        :param mode: Specifies the ouput mode of the LUT waveform as follows:

            0x01 - Output Continuous - The waveform is output continuously
            (i.e. until a StopOPLut command is received.)

            0x02 - Output Fixed - A fixed number of waveform cycles are output
            (as specified in the num_cycles parameter).
        :param cycle_length: Specifies how many samples will be output in each
            cycle of the waveform. It can be set in the range [0; 512]
            (for TPZ). It must be less than or equal to the total number of
            samples that were loaded.
        :param num_cycles: Specifies the number of cycles (1 to 2147483648) to
            be output when the Mode parameter is set to fixed. If Mode is set
            to Continuous, the num_cycles parameter is ignored. In both cases,
            the waveform is not output until a StartOPLUT command is received.
        :param delay_time: Specifies the delay (in sample intervals) that the
            system waits after setting each LUT output value. By default, the
            time the system takes to output LUT values (sampling interval) is
            set at the maximum bandwidth possible, i.e. 4 kHz (0.25 ms) for TPZ
            units. The delay_time parameter specifies the time interval between
            neighbouring samples, i.e. for how long the sample will remain at
            its present value. To increase the time between samples, set the
            delay_time parameter to the required additional delay (1 to
            2147483648 sample intervals). In this way, the user can stretch or
            shrink the waveform without affecting its overall shape.
        :param precycle_rest: In some applications, during waveform generation
            the first and the last samples may need to be handled differently
            from the rest of the waveform. For example, in a positioning system
            it may be necessary to start the movement by staying at a certain
            position for a specified length of time, then perform a movement,
            then remain at the last position for another specified length of
            time. This is the purpose of precycle_rest and postcycle_rest
            parameters, i.e. they specify the length of time that the first and
            last samples are output for, independently of the delay_time
            parameter. The precycle_rest parameter allows a delay time to be
            set before the system starts to clock out the LUT values. The delay
            can be set between 0 and 2147483648 sample intervals. The system
            then outputs the first value in the LUT until the PreCycleRest time
            has expired.
        :param postcycle_rest: In a similar way to precycle_rest, the
            postcycle_rest parameter specifies the delay imposed by the system
            after a LUT table has been output. The delay can be set between 0
            and 2147483648 sample intervals. The system then outputs the last
            value in the cycle until the postcycle_rest time has expired.
        """
        # triggering is not supported by the TPZ device
        payload = st.pack(
            "<HHHLLLLHLH",
            Tpz._CHANNEL,
            mode,
            cycle_length,
            num_cycles,
            delay_time,
            precycle_rest,
            postcycle_rest,
            0,
            0,
            0,
        )
        await self.send(Message(MGMSG.PZ_SET_OUTPUTLUTPARAMS, data=payload))

    async def get_output_lut_parameters(self) -> tuple[int, int, int, int, int, int]:
        """Get Waveform Generator Mode parameters.

        :return: a 6 int elements tuple whose members are (mode, cycle_length,
            num_cycles, delay_time, precycle_rest, postcycle_rest).
        :rtype: 6 int elements tuple
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_OUTPUTLUTPARAMS,
            [MGMSG.PZ_GET_OUTPUTLUTPARAMS],
            Tpz._CHANNEL,
        )
        return st.unpack("<HHLLLL", get_msg.data[2:22])

    async def start_lut_output(self) -> None:
        """Start the voltage waveform (LUT) outputs."""
        await self.send(Message(MGMSG.PZ_START_LUTOUTPUT, param1=Tpz._CHANNEL))

    async def stop_lut_output(self) -> None:
        """Stop the voltage waveform (LUT) outputs."""
        await self.send(Message(MGMSG.PZ_STOP_LUTOUTPUT, param1=Tpz._CHANNEL))

    async def set_eeprom_parameters(self, msg_id: int) -> None:
        """Save the parameter settings for the specified message.

        :param msg_id: The message ID of the message containing the parameters
            to be saved.
        """
        payload = st.pack("<HH", Tpz._CHANNEL, msg_id)
        await self.send(Message(MGMSG.PZ_SET_EEPROMPARAMS, data=payload))

    async def set_tpz_display_settings(self, intensity: int) -> None:
        """Set the intensity of the LED display on the front of the TPZ unit.

        :param intensity: The intensity is set as a value from 0 (Off) to 255
            (brightest).
        """
        payload = st.pack("<H", intensity)
        await self.send(Message(MGMSG.PZ_SET_TPZ_DISPSETTINGS, data=payload))

    async def get_tpz_display_settings(self) -> int:
        """Get the intensity of the LED display on the front of the TPZ unit.

        :return: The intensity as a value from 0 (Off) to 255 (brightest).
        :rtype: int
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_TPZ_DISPSETTINGS, [MGMSG.PZ_GET_TPZ_DISPSETTINGS], Tpz._CHANNEL
        )
        return st.unpack("<H", get_msg.data)[0]

    async def set_tpz_io_settings(
        self, voltage_limit: int, hub_analog_input: int
    ) -> None:
        """Set various I/O settings.

        :param voltage_limit: The piezo actuator connected to the T-Cube has a
            specific maximum operating voltage. This parameter sets the maximum
            output to the value among the following ones:

            75 V limit.

            100 V limit.

            150 V limit.
        :param hub_analog_input: When the T-Cube piezo driver unit is used in
            conjunction with the T-Cube Strain Gauge Reader (TSG001) on the
            T-Cube Controller Hub (TCH001), a feedback signal can be passed
            from the Strain Gauge Reader to the Piezo unit.
            High precision closed loop operation is then possible using the
            complete range of feedback-equipped piezo actuators.
            This parameter is routed to the Piezo unit as follows:

            0x01: the feedback signals run through all T-Cube bays.

            0x02: the feedback signals run between adjacent pairs of T-Cube
            bays (i.e. 1&2, 3&4, 5&6). This setting is useful when several
            pairs of Strain Gauge/Piezo Driver cubes are being used on the same
            hub.

            0x03: the feedback signals run through the read panel SMA
            connectors.
        """
        self.voltage_limit = voltage_limit

        if self.voltage_limit == 75:
            voltage_limit = 1
        elif self.voltage_limit == 100:
            voltage_limit = 2
        elif self.voltage_limit == 150:
            voltage_limit = 3
        else:
            raise ValueError("voltage_limit must be 75 V, 100 V or 150 V")

        payload = st.pack(
            "<HHHHH",
            Tpz._CHANNEL,
            voltage_limit,
            hub_analog_input,
            Tpz._RESERVED,
            Tpz._RESERVED,
        )
        await self.send(Message(MGMSG.PZ_SET_TPZ_IOSETTINGS, data=payload))

    async def get_tpz_io_settings(self) -> tuple[int, int]:
        """Get various I/O settings.

        :return: Returns a tuple whose elements are the voltage limit and the
            Hub analog input. Refer to :py:meth:`set_tpz_io_settings()`
            <Tpz.set_tpz_io_settings>` for
            the meaning of those parameters.
        :rtype: a 2 elements tuple (int, int)
        """
        get_msg = await self.send_request(
            MGMSG.PZ_REQ_TPZ_IOSETTINGS, [MGMSG.PZ_GET_TPZ_IOSETTINGS], Tpz._CHANNEL
        )
        voltage_limit, hub_analog_input = st.unpack("<HH", get_msg.data[2:6])
        if voltage_limit == 1:
            voltage_limit = 75
        elif voltage_limit == 2:
            voltage_limit = 100
        elif voltage_limit == 3:
            voltage_limit = 150
        else:
            raise ValueError("Voltage limit should be in range [1; 3]")
        self.voltage_limit = voltage_limit
        return voltage_limit, hub_analog_input


class TpzSim:
    def __init__(self) -> None:
        self.voltage_limit: int = 150
        self.hub_analog_input: int = 1

    def close(self) -> None:
        pass

    def module_identify(self) -> None:
        pass

    def set_position_control_mode(self, control_mode: int) -> None:
        self.control_mode: int = control_mode

    def get_position_control_mode(self) -> int:
        return self.control_mode

    def set_output_volts(self, voltage: float) -> None:
        self.voltage: float = voltage

    def get_output_volts(self) -> float:
        return self.voltage

    def set_output_position(self, position_sw: int) -> None:
        self.position_sw: int = position_sw

    def get_output_position(self) -> int:
        return self.position_sw

    def set_input_volts_source(self, volt_src: int) -> None:
        self.volt_src: int = volt_src

    def get_input_volts_source(self) -> int:
        return self.volt_src

    def set_pi_constants(self, prop_const: int, int_const: int) -> None:
        self.prop_const: int = prop_const
        self.int_const: int = int_const

    def get_pi_constants(self) -> tuple[int, int]:
        return self.prop_const, self.int_const

    def set_output_lut(self, lut_index: int, output: float) -> None:
        if lut_index < 0 or lut_index > 512:
            raise ValueError(
                "LUT index should be in range [0;512] and not {}".format(lut_index)
            )
        self.lut: list[float] = [0.0] * 513
        self.lut[lut_index] = output

    def get_output_lut(self) -> tuple[int, float]:
        return 0, 0.0  # FIXME: the API description here doesn't make any sense

    def set_output_lut_parameters(
        self,
        mode: int,
        cycle_length: int,
        num_cycles: int,
        delay_time: int,
        precycle_rest: int,
        postcycle_rest: int,
    ) -> None:
        self.mode: int = mode
        self.cycle_length: int = cycle_length
        self.num_cycles: int = num_cycles
        self.delay_time: int = delay_time
        self.precycle_rest: int = precycle_rest
        self.postcycle_rest: int = postcycle_rest

    def get_output_lut_parameters(self) -> tuple[int, int, int, int, int, int]:
        return (
            self.mode,
            self.cycle_length,
            self.num_cycles,
            self.delay_time,
            self.precycle_rest,
            self.postcycle_rest,
        )

    def start_lut_output(self) -> None:
        pass

    def stop_lut_output(self) -> None:
        pass

    def set_eeprom_parameters(self, msg_id: int) -> None:
        pass

    def set_tpz_display_settings(self, intensity: int) -> None:
        self.intensity: int = intensity

    def get_tpz_display_settings(self) -> int:
        return self.intensity

    def set_tpz_io_settings(self, voltage_limit: int, hub_analog_input: int) -> None:
        if voltage_limit not in [75, 100, 150]:
            raise ValueError("voltage_limit must be 75 V, 100 V or 150 V")
        self.voltage_limit = voltage_limit
        self.hub_analog_input = hub_analog_input

    def get_tpz_io_settings(self) -> tuple[int, int]:
        return self.voltage_limit, self.hub_analog_input
