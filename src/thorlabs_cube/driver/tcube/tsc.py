import struct as st

from thorlabs_cube.driver.base import _Cube
from thorlabs_cube.driver.message import MGMSG, Message, MsgError


class Tsc(_Cube):
    """TSC001 T-Cube Motor Controller class"""

    def __init__(self, serial_dev):
        super().__init__(serial_dev)
        self.status_report_counter = 0

    async def handle_message(self, msg) -> None:
        msg_id = msg.id
        data = msg.data

        if msg_id == MGMSG.HW_DISCONNECT:
            raise MsgError("Error: Please disconnect the TSC001")
        elif msg_id == MGMSG.HW_RESPONSE:
            raise MsgError("Hardware error, please disconnect and reconnect the TSC001")
        elif msg_id == MGMSG.HW_RICHRESPONSE:
            (code,) = st.unpack("<H", data[2:4])
            raise MsgError(
                "Hardware error {}: {}".format(code, data[4:].decode(encoding="ascii"))
            )
        elif (
            msg_id == MGMSG.MOT_MOVE_COMPLETED
            or msg_id == MGMSG.MOT_MOVE_STOP
            or msg_id == MGMSG.MOT_GET_STATUSUPDATE
        ):
            if self.status_report_counter == 25:
                self.status_report_counter = 0
                await self.send(Message(MGMSG.MOT_MOVE_COMPLETED))
            else:
                self.status_report_counter += 1
            (
                self.position,
                self.encoder_count,
                self.status_bits,
                self.chan_identity_two,
                _,
                _,
                _,
            ) = st.unpack(
                "<LLLHLLL",
                data[2:],
            )

    async def get_bay_used(self) -> int:
        """Identify which bay is being used by the controller on Thorlabs Hub

        :return: Integer representing the bay being used on the Thorlabs Hub
        """
        get_msg = await self.send_request(
            MGMSG.HUB_REQ_BAYUSED, [MGMSG.HUB_GET_BAYUSED], Tsc._CHANNEL
        )

        return get_msg.param1

    async def set_absolute_position(self, absolute_position: int) -> None:
        """Move the motor to an absolute position.

        :param absolute_position: The absolute position in encoder counts.
                                E.g., 200,000 counts for 10 mm.
        """
        payload = st.pack("<Hl", Tsc._CHANNEL, absolute_position)

        await self.send_request(
            MGMSG.MOT_MOVE_ABSOLUTE,
            [MGMSG.MOT_MOVE_COMPLETED, MGMSG.MOT_MOVE_STOPPED],
            data=payload,
        )

    async def move_stop(self, stop_mode: int) -> None:
        """Stop any type of motor move (relative, absolute, homing, or velocity).

        :param stop_mode: The stop mode (1 for immediate stop, 2 for profiled stop).
        """
        await self.send_request(
            MGMSG.MOT_MOVE_STOP,
            [MGMSG.MOT_MOVE_STOPPED],
            param1=Tsc._CHANNEL,
            param2=stop_mode,
        )

    async def set_av_modes(self, mode_bits: int) -> None:
        """Set the LED indicator modes based on the provided mode_bits.

        :param mode_bits: A bitmask indicating which modes to enable:
                        - 1 (LEDMODE_IDENT): LED flashes when 'Ident' is sent.
                        - 2 (LEDMODE_LIMITSWITCH): LED flashes when motor reaches limit switch.
                        - 8 (LEDMODE_MOVING): LED is lit when the motor is moving.
        """
        payload = st.pack("<Hl", Tsc._CHANNEL, mode_bits)
        await self.send(Message(MGMSG.MOT_SET_AVMODES, data=payload))

    async def get_av_modes(self) -> int:
        """Get the current LED indicator mode bits set by set_av_modes(self, mode_bits)

        :return: The LED mode bits set
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_AVMODES, [MGMSG.MOT_GET_AVMODES], Tsc._CHANNEL
        )

        return get_msg.data[2:]

    async def set_button_parameters(
        self, mode: int, position1: int, position2: int, timeout1: int, timeout2: int
    ) -> None:
        """Set button parameters for the front panel buttons.

        :param mode: Mode for the buttons (1 for jog, 2 for position mode).
        :param position1: Position in encoder counts for the top button.
        :param position2: Position in encoder counts for the bottom button.
        :param timeout1: Timeout in ms for position1.
        :param timeout2: Timeout in ms for position2.
        """
        payload = st.pack(
            "<HHllHH", Tsc._CHANNEL, mode, position1, position2, timeout1, timeout2
        )

        await self.send(Message(MGMSG.MOT_SET_BUTTONPARAMS, data=payload))

    async def get_button_parameters(self) -> tuple[int, int, int, int, int]:
        """Get the current button parameters.

        :return: A tuple containing (mode, position1, position2, timeout1, timeout2)
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_BUTTONPARAMS, [MGMSG.MOT_GET_BUTTONPARAMS], Tsc._CHANNEL
        )

        return st.unpack("<HllHH", get_msg.data[2:])

    async def set_eeprom_parameters(self, msg_id: int) -> None:
        """Save the current parameters for the specified message in the EEPROM.

        This function sends a request to the device to save the parameter settings
        of the specified message to the EEPROM memory, ensuring the settings are
        retained even after the device is powered off.

        :param msg_id: The message ID of the message containing the parameters
                       that need to be saved in the EEPROM.
        """
        payload = st.pack("<HH", Tsc._CHANNEL, msg_id)

        await self.send(Message(MGMSG.MOT_SET_EEPROMPARAMS, data=payload))

    async def get_status_update(self) -> tuple[int, int, int, int]:
        """Returns a status update on the specified motor channel

        This function sends a request to the device to return status updates of
        position, encoder count, status bits on channel one as well as, for future use,
        returns channel identity two and its associated data which is garbage right now

        :return: A tuple containing (position, encoder_count, status_bits, chan_identity_two)
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_STATUSUPDATE, [MGMSG.MOT_GET_STATUSUPDATE], Tsc._CHANNEL
        )
        (
            position,
            encoder_count,
            status_bits,
            chan_identity_two,
            _,
            _,
            _,
        ) = st.unpack("<HIIIHIII", get_msg.data[2:])

        return position, encoder_count, status_bits, chan_identity_two

    async def set_sol_operating_mode(self, operating_mode: int) -> None:
        """Set the solenoid operating mode for the single channel.

        :param operating_mode: The operating mode to set (e.g., 1, 2, etc.).
        """
        await self.send(Message(MGMSG.MOT_SET_SOL_OPERATINGMODE, param2=operating_mode))

    async def get_sol_operating_mode(self) -> int:
        """Get the current solenoid operating mode for the single channel.

        :return: Operating mode of solenoid represented by an integer
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_SOL_OPERATINGMODE,
            [MGMSG.MOT_GET_SOL_OPERATINGMODE],
            param1=Tsc._CHANNEL,
        )

        return get_msg.param2

    async def set_solenoid_cycle_parameters(
        self, on_time: int, off_time: int, num_cycles: int
    ) -> None:
        """Set the solenoid cycle parameters.

        :param on_time: Time (in ms) the solenoid stays on (100ms to 10,000ms).
        :param off_time: Time (in ms) the solenoid stays off (100ms to 10,000ms).
        :param num_cycles: Number of open/close cycles (0 for infinite, up to 1,000,000).
        """
        payload = st.pack("<HLLL", Tsc._CHANNEL, on_time, off_time, num_cycles)
        await self.send(Message(MGMSG.MOT_SET_SOL_CYCLEPARAMS, data=payload))

    async def get_solenoid_cycle_parameters(self) -> tuple[int, int, int]:
        """Get the current solenoid cycle parameters.

        :return: A tuple containing (on_time, off_time, num_cycles).
        """
        payload = st.pack("<H", Tsc._CHANNEL)
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_SOL_CYCLEPARAMS, [MGMSG.MOT_GET_SOL_CYCLEPARAMS], data=payload
        )

        return st.unpack("<LLL", get_msg.data[2:])

    async def set_sol_interlock_mode(self, mode: int) -> None:
        """Set the solenoid interlock mode.

        :param mode: Interlock mode, where:
                    - 0x01 = SOLENOID_ENABLED (hardware interlock required)
                    - 0x02 = SOLENOID_DISABLED (hardware interlock not required)
        """
        await self.send(Message(MGMSG.MOT_SET_SOL_INTERLOCKMODE, param2=mode))

    async def get_sol_interlock_mode(self) -> int:
        """Get the current solenoid interlock mode.

        :return: The interlock mode, where:
                - 0x01 = SOLENOID_ENABLED (hardware interlock required)
                - 0x02 = SOLENOID_DISABLED (hardware interlock not required)
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_SOL_INTERLOCKMODE,
            [MGMSG.MOT_GET_SOL_INTERLOCKMODE],
            param1=Tsc._CHANNEL,
        )

        return get_msg.param2

    async def set_sol_state(self, state: int) -> None:
        """Set the solenoid state (ON or OFF).

        :param state: The solenoid state, where:
                    - 0x01 = SOLENOID_ON (solenoid is active).
                    - 0x02 = SOLENOID_OFF (solenoid is deactivated).
        """
        await self.send(
            Message(MGMSG.MOT_SET_SOL_STATE, param1=Tsc._CHANNEL, param2=state)
        )

    async def get_sol_state(self) -> int:
        """Get the current solenoid state.

        :return: The solenoid state, where:
                - 0x01 = SOLENOID_ON (solenoid is active).
                - 0x02 = SOLENOID_OFF (solenoid is deactivated).
        """
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_SOL_STATE, [MGMSG.MOT_GET_SOL_STATE], param1=Tsc._CHANNEL
        )

        return get_msg.param2


class TscSim:
    def __init__(self, position, encoder_count, status_bits, chan_identity_two) -> None:
        self.position = position
        self.encoder_count = encoder_count
        self.status_bits = status_bits
        self.chan_identity_two = chan_identity_two

    def module_identify(self) -> None:
        pass

    def get_bay_used(self) -> int:
        return 0

    def set_absolute_position(self, absolute_position: int) -> None:
        self.absolute_position = absolute_position

    def move_stop(self, stop_mode: int) -> None:
        self.stop_mode = stop_mode

    def set_av_modes(self, mode_bits: int) -> None:
        self.mode_bits = mode_bits

    def get_av_modes(self) -> int:
        return self.mode_bits

    def set_button_parameters(
        self, mode: int, position1: int, position2: int, timeout1: int, timeout2: int
    ) -> None:
        self.mode = mode
        self.position1 = position1
        self.position2 = position2
        self.timeout1 = timeout1
        self.timeout2 = timeout2

    def get_button_parameters(self) -> tuple[int, int, int, int, int]:
        return self.mode, self.position1, self.position2, self.timeout1, self.timeout2

    def set_eeprom_parameters(self, msg_id: int) -> None:
        self.msg_id = msg_id

    def get_status_update(
        self,
    ) -> tuple[
        int, int, int, int
    ]:  # TODO: not implemented yet for simulation, need to make the framework to mock this data
        return (
            self.position,
            self.encoder_count,
            self.status_bits,
            self.chan_identity_two,
        )

    def set_sol_operating_mode(self, operating_mode: int) -> None:
        self.operating_mode = operating_mode

    def get_sol_operating_mode(self) -> int:
        return self.operating_mode

    def set_solenoid_cycle_parameters(
        self, on_time: int, off_time: int, num_cycles: int
    ) -> None:
        self.on_time = on_time
        self.off_time = off_time
        self.num_cycles = num_cycles

    def get_solenoid_cycle_parameters(self) -> tuple[int, int, int]:
        return (self.on_time, self.off_time, self.num_cycles)

    def set_sol_interlock_mode(self, mode: int) -> None:
        self.interlock_mode = mode

    def get_sol_interlock_mode(self) -> int:
        return self.interlock_mode

    def set_sol_state(self, state: int) -> None:
        self.sol_state = state

    def get_sol_state(self) -> int:
        return self.sol_state
