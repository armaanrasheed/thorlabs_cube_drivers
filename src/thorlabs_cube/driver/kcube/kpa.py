import struct as st
from typing import Tuple

from thorlabs_cube.driver.message import MGMSG, QUADMSG, Message, MsgError
from thorlabs_cube.driver.tcube.tpa import Tpa, TpaSim


class Kpa(Tpa):
    """KPA101 Position Sensing Detector Auto Aligner driver implementation."""

    def __init__(self, serial_dev: str) -> None:
        """Initialize the KPA101 driver.

        :param serial_dev: Serial device identifier.
        """
        super().__init__(serial_dev)
        self.loop_params = None
        self.status_report_counter = 0

    async def handle_message(self, msg: Message) -> None:
        """Handle incoming messages from the KPA101 device.

        :param msg: Message object received from the device.
        """
        msg_id = msg.id
        data = msg.data

        if msg_id == MGMSG.HW_DISCONNECT:
            raise MsgError("Error: Please disconnect the KPA101")

        elif msg_id == MGMSG.HW_RESPONSE:
            raise MsgError("Hardware error, please disconnect and reconnect the KPA101")

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

    async def set_trigger_config(
        self,
        trig1_mode: int,
        trig1_polarity: int,
        trig1_sum_min: int,
        trig1_sum_max: int,
        trig1_diff_threshold: int,
        trig2_mode: int,
        trig2_polarity: int,
        trig2_sum_min: int,
        trig2_sum_max: int,
        trig2_diff_threshold: int,
    ) -> None:
        """Set trigger configuration for both TRIG1 and TRIG2.

        :param trig1_mode: TRIG1 operating mode.
        :param trig1_polarity: TRIG1 polarity.
        :param trig1_sum_min: TRIG1 sum minimum.
        :param trig1_sum_max: TRIG1 sum maximum.
        :param trig1_diff_threshold: TRIG1 differential threshold.
        :param trig2_mode: TRIG2 operating mode.
        :param trig2_polarity: TRIG2 polarity.
        :param trig2_sum_min: TRIG2 sum minimum.
        :param trig2_sum_max: TRIG2 sum maximum.
        :param trig2_diff_threshold: TRIG2 differential threshold.
        """

        payload = st.pack(
            "<HHHHHHHHHHHHHH",
            QUADMSG.QUAD_KPA_TRIGIO_SUB_ID.value,
            trig1_mode,
            trig1_polarity,
            trig1_sum_min,
            trig1_sum_max,
            trig1_diff_threshold,
            trig2_mode,
            trig2_polarity,
            trig2_sum_min,
            trig2_sum_max,
            trig2_diff_threshold,
            Kpa._RESERVED,
            Kpa._RESERVED,
            Kpa._RESERVED,
        )
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_trigger_config(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int, int, int, int]:
        """Get trigger configuration for both TRIG1 and TRIG2.

        :return: A tuple containing trigger configuration parameters for TRIG1 and TRIG2.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_KPA_TRIGIO_SUB_ID.value,
        )

        return st.unpack("<HHHHHHHHHHHHHHHHH", get_msg.data)[1:]

    async def set_digital_outputs(self, trigOne: int, trigTwo: int) -> None:
        """Set digital outputs for TRIG1 and TRIG2.

        :param digital_outputs: Status of TRIG1 and TRIG2 outputs.
        """
        payload = st.pack(
            "<HBBH",
            QUADMSG.QUAD_KPA_DIGOPS_SUB_ID.value,
            trigOne,
            trigTwo,
            Kpa._RESERVED,
        )
        await self.send(Message(MGMSG.QUAD_SET_PARAMS, data=payload))

    async def get_digital_outputs(self) -> Tuple[int, int]:
        """Get digital outputs for TRIG1 and TRIG2.

        :return: Status of TRIG1 and TRIG2 outputs.
        """
        get_msg = await self.send_request(
            MGMSG.QUAD_REQ_PARAMS,
            [MGMSG.QUAD_GET_PARAMS],
            param1=QUADMSG.QUAD_KPA_DIGOPS_SUB_ID.value,
        )
        return st.unpack("<HHHHHHHH", get_msg.data)[1]


class KpaSim(TpaSim):
    """Simulation class for KPA101."""

    def __init__(self):
        self.trigger_config = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.digital_outputs = 0x00

    def close(self):
        pass

    def set_trigger_config(
        self,
        trig1_mode: int,
        trig1_polarity: int,
        trig1_sum_min: int,
        trig1_sum_max: int,
        trig1_diff_threshold: int,
        trig2_mode: int,
        trig2_polarity: int,
        trig2_sum_min: int,
        trig2_sum_max: int,
        trig2_diff_threshold: int,
    ) -> None:

        self.trigger_config = (
            trig1_mode,
            trig1_polarity,
            trig1_sum_min,
            trig1_sum_max,
            trig1_diff_threshold,
            trig2_mode,
            trig2_polarity,
            trig2_sum_min,
            trig2_sum_max,
            trig2_diff_threshold,
        )

    def get_trigger_config(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        return self.trigger_config

    def set_digital_outputs(self, digital_outputs: int) -> None:
        self.digital_outputs = digital_outputs

    def get_digital_outputs(self) -> int:
        return self.digital_outputs
