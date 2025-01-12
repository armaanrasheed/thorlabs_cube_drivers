import struct as st

from thorlabs_cube.driver.base import _Cube
from thorlabs_cube.driver.message import MGMSG, QUADMSG, Message, MsgError


class Tpa(_Cube):
    """TPA101 Position Sensing Detector driver implementation."""

    def __init__(self, serial_dev: str) -> None:
        """Initialize the TPA101 driver.

        :param serial_dev: Serial device identifier.
        """
        super().__init__(serial_dev)
        self.loop_params = None
        self.status_report_counter = 0

    async def handle_message(self, msg: Message) -> None:
        """Handle incoming messages from the TPA101 device.

        :param msg: Message object received from the device.
        """
        msg_id: MGMSG = msg.id
        data: bytes = msg.data

        if msg_id == MGMSG.HW_DISCONNECT:
            raise MsgError("Error: Please disconnect the TPA101")

        elif msg_id == MGMSG.HW_RESPONSE:
            raise MsgError("Hardware error, please disconnect and reconnect the TPA101")

        elif msg_id == MGMSG.QUAD_GET_STATUSUPDATE:
            x_diff, y_diff, sum_val, x_pos, y_pos, status_bits = st.unpack(
                "<hhIhhI", data[6:20]
            )

            # Update internal state variables with the extracted values
            self.x_diff = x_diff
            self.y_diff = y_diff
            self.sum_val = sum_val
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.status_bits = status_bits

            if self.status_report_counter == 25:
                self.status_report_counter = 0
                await self.send(Message(MGMSG.QUAD_ACK_STATUSUPDATE))
            else:
                self.status_report_counter += 1

    async def set_loop_params(self, p_gain: int, i_gain: int, d_gain: int) -> None:
        """Set proportional, integral, and differential feedback loop constants.

        :param p_gain: Proportional gain value.
        :param i_gain: Integral gain value.
        :param d_gain: Differential gain value.
        """
        payload = st.pack(
            "<HHHH", QUADMSG.QUAD_LOOP_PARAMS_SUB_ID.value, p_gain, i_gain, d_gain
        )
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_loop_params(self) -> tuple[int, int, int]:
        """Get proportional, integral, and differential feedback loop constants.

        :return: A tuple containing p_gain, i_gain, and d_gain values.
        """

        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_LOOP_PARAMS_SUB_ID.value,
        )
        return st.unpack("<HHHH", get_msg.data)[1:]

    async def set_quad_oper_mode(self, mode: int) -> None:
        """Set the operating mode of the unit.

        :param mode: 1 for Monitor Mode, 2 for Open Loop, 3 for Closed Loop.
        """

        payload = st.pack("<HH", QUADMSG.QUAD_OPER_MODE_SUB_ID.value, mode)
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_quad_oper_mode(self) -> int:
        """Get the operating mode of the unit.

        :return: The current operating mode of the unit.
        """

        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_OPER_MODE_SUB_ID.value,
        )
        return st.unpack("<HH", get_msg.data)[1]

    async def set_quad_position_demand_params(
        self,
        x_pos_min: int,
        x_pos_max: int,
        y_pos_min: int,
        y_pos_max: int,
        low_volt_output_route: int,
        open_loop_pos_demands: int,
        x_pos_demand_feedback_sense: float,
        y_pos_demand_feedback_sense: float,
    ) -> None:
        """Set position demand parameters for the quad system.

        :param x_pos_min: Minimum X-axis position demand.
        :param x_pos_max: Maximum X-axis position demand.
        :param y_pos_min: Minimum Y-axis position demand.
        :param y_pos_max: Maximum Y-axis position demand.
        :param low_volt_output_route: LV output signal routing
        :param open_loop_pos_demands: Open loop position demands configuration
        :param x_pos_demand_feedback_sense: Signal sense and gain for X-axis output
        :param y_pos_demand_feedback_sense: Signal sense and gain for Y-axis output
        """
        payload = st.pack(
            "<hhhhhhhhh",
            QUADMSG.QUAD_POSITION_DEMAND_PARAMS_SUB_ID.value,
            x_pos_min,
            x_pos_max,
            y_pos_min,
            y_pos_max,
            low_volt_output_route,
            open_loop_pos_demands,
            x_pos_demand_feedback_sense,
            y_pos_demand_feedback_sense,
        )
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_quad_position_demand_params(self) -> tuple[int, int, int, int]:
        """Get position demand parameters for the quad system.

        :return: A tuple containing x_pos_min, x_pos_max, y_pos_min, and y_pos_max.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_POSITION_DEMAND_PARAMS_SUB_ID.value,
        )
        return st.unpack("<hhhhhhhhh", get_msg.data)[1:]

    async def get_quad_status_bits(self) -> int:
        """Get the status bits of the control unit.

        :return: Status bits of the control unit.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_STATUS_BITS_SUB_ID.value,
        )
        return st.unpack("<HI", get_msg.data)[1]

    async def get_quad_readings(self) -> tuple[int, int, int, int, int]:
        """Get the status bits of the quad readings.

        :return: Status bits of the quad reading.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_READINGS_SUB_ID.value,
        )
        return st.unpack("HHHHHH", get_msg.data)[1:]

    async def set_quad_display_settings(
        self, disp_intensity: int, disp_mode: int, disp_dim_timeout: int
    ) -> None:
        """Set the display settings for the quad system.

        :param disp_intensity: Display intensity (0-255).
        :param disp_mode: Display mode (1 for Difference, 2 for Position).
        :param disp_dim_timeout: Dim timeout value as per documentation.
        """
        payload = st.pack(
            "<HHHH",
            QUADMSG.QUAD_DISP_SETTINGS_SUB_ID.value,
            disp_intensity,
            disp_mode,
            disp_dim_timeout,
        )
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_quad_display_settings(self) -> tuple[int, int, int]:
        """Get the display settings for the quad system.

        :return: A tuple containing disp_intensity, disp_mode, and disp_dim_timeout.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_DISP_SETTINGS_SUB_ID.value,
        )
        return st.unpack("<HHHH", get_msg.data)[1:]

    async def set_quad_position_outputs(self, x_pos: int, y_pos: int) -> None:
        """Set the X and Y position outputs.

        :param x_pos: X-axis position output value (-32768 to 32767).
        :param y_pos: Y-axis position output value (-32768 to 32767).
        """
        payload = st.pack(
            "<HHH", QUADMSG.QUAD_POSITION_OUTPUTS_SUB_ID.value, x_pos, y_pos
        )
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_quad_position_outputs(self) -> tuple[int, int]:
        """Get the X and Y position outputs.

        :return: A tuple containing x_pos and y_pos.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_POSITION_OUTPUTS_SUB_ID.value,
        )
        return st.unpack("<Hhh", get_msg.data)[1:]

    async def set_quad_loop_params_two(
        self,
        p_gain: float,
        i_gain: float,
        d_gain: float,
        d_cutoff_freq: float,
        notch_freq: float,
        filter_q: float,
        notch_on: int,
        deriv_filter_on: int,
    ) -> None:
        """Set the extended loop parameters for the quad system.

        :param p_gain: Proportional gain value.
        :param i_gain: Integral gain value.
        :param d_gain: Differential gain value.
        :param d_cutoff_freq: Differential cutoff frequency.
        :param notch_freq: Notch filter frequency.
        :param filter_q: Filter quality factor.
        :param notch_on: Notch filter on/off flag.
        :param deriv_filter_on: Derivative filter on/off flag.
        """
        payload = st.pack(
            "<HFFFFFFHH",
            QUADMSG.QUAD_LOOP_PARAMS_TWO_SUB_ID.value,
            p_gain,
            i_gain,
            d_gain,
            d_cutoff_freq,
            notch_freq,
            filter_q,
            notch_on,
            deriv_filter_on,
        )
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_quad_loop_params_two(
        self,
    ) -> tuple[float, float, float, float, float, float, int, int]:
        """Get the extended loop parameters for the quad system.

        :return: A tuple containing p_gain, i_gain, d_gain, d_cutoff_freq,
        notch_freq, filter_q, notch_on, deriv_filter_on.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_LOOP_PARAMS_TWO_SUB_ID.value,
        )
        return st.unpack("<HFFFFFFHH", get_msg.data)

    async def set_eeprom_params(self, msg_id: int) -> None:
        """Save the parameter settings for the specified message.

        :param msg_id: The message ID of the message containing the parameters to be saved.
        """
        payload = st.pack("<H", msg_id)
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))


class TpaSim:
    """Simulation class for TPA101."""

    def __init__(self):

        self.loop_params = (0, 0, 0)
        self.quad_readings = (0, 0, 0, 0, 0)
        self.pos_demand_params = (0, 0, 0, 0, 2, 0, 0, 0)
        self.oper_mode = 1
        self.status_bits = 0x00000001
        self.display_settings = (255, 1, 2570)
        self.position_outputs = (0, 0)
        self.loop_params2 = (0, 0, 0, 0, 0, 0.1, 2, 2)
        self.eeprom_params = 0x00

    def close(self):
        pass

    def set_loop_params(self, p_gain: int, i_gain: int, d_gain: int) -> None:
        self.loop_params = (p_gain, i_gain, d_gain)

    def get_loop_params(self) -> tuple[int, int, int]:
        return self.loop_params

    def set_quad_oper_mode(self, mode: int) -> None:
        self.oper_mode = mode

    def get_quad_oper_mode(self) -> int:
        return self.oper_mode

    def set_quad_position_demand_params(
        self,
        x_pos_min: int,
        x_pos_max: int,
        y_pos_min: int,
        y_pos_max: int,
        low_volt_output_route: int,
        open_loop_pos_demands: int,
        x_pos_demand_feedback_sense: float,
        y_pos_demand_feedback_sense: float,
    ) -> None:

        self.pos_demand_params = (
            x_pos_min,
            x_pos_max,
            y_pos_min,
            y_pos_max,
            low_volt_output_route,
            open_loop_pos_demands,
            x_pos_demand_feedback_sense,
            y_pos_demand_feedback_sense,
        )

    def get_quad_position_demand_params(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int]:

        return self.pos_demand_params

    def get_quad_status_bits(self) -> int:

        return self.status_bits

    def set_quad_display_settings(
        self, disp_intensity: int, disp_mode: int, disp_dim_timeout: int
    ) -> None:

        self.display_settings = (disp_intensity, disp_mode, disp_dim_timeout)

    def get_quad_display_settings(self) -> tuple[int, int, int]:
        return self.display_settings

    def set_quad_position_outputs(self, x_pos: int, y_pos: int) -> None:

        self.position_outputs = (x_pos, y_pos)

    def get_quad_position_outputs(self) -> tuple[int, int]:
        return self.position_outputs

    def set_quad_loop_params2(
        self,
        p_gain: float,
        i_gain: float,
        d_gain: float,
        d_cutoff_freq: float,
        notch_freq: float,
        filter_q: float,
        notch_on: int,
        deriv_filter_on: int,
    ) -> None:

        self.loop_params2 = (
            p_gain,
            i_gain,
            d_gain,
            d_cutoff_freq,
            notch_freq,
            filter_q,
            notch_on,
            deriv_filter_on,
        )

    def get_quad_loop_params2(
        self,
    ) -> tuple[float, float, float, float, float, float, int, int]:
        return self.loop_params2
