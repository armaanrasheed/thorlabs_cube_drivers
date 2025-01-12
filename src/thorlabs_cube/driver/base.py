import asyncio
import logging
import struct as st

import asyncserial

from thorlabs_cube.driver.message import MGMSG, Message, MsgError

logger = logging.getLogger(__name__)


class _Cube:
    _RESERVED: int = 0x00
    _CHANNEL: int = 0x01
    _REQUEST_LENGTH: int = 1

    def __init__(self, serial_dev):
        self.port = asyncserial.AsyncSerial(serial_dev, baudrate=115200, rtscts=True)

    def close(self):
        """Close the device."""
        self.port.close()

    async def send(self, message):
        logger.debug("sending: %s", message)
        await self.port.write(message.pack())

    async def recv(self):
        header = await self.port.read_exactly(6)
        logger.debug("received header: %s", header)
        data = b""
        if header[4] & 0x80:
            (length,) = st.unpack("<H", header[2:4])
            data = await self.port.read_exactly(length)
        r = Message.unpack(header + data)
        logger.debug("receiving: %s", r)
        return r

    async def handle_message(self, msg):
        # derived classes must implement this
        raise NotImplementedError

    async def send_request(
        self, msgreq_id, wait_for_msgs, param1=0, param2=0, data=None
    ):
        await self.send(Message(msgreq_id, param1, param2, data=data))
        msg = None
        while msg is None or msg.id not in wait_for_msgs:
            msg = await self.recv()
            await self.handle_message(msg)
        return msg

    async def set_channel_enable_state(self, activated):
        """Enable or Disable channel 1.

        :param activated: 1 to enable channel, 0 to disable it.
        """

        if activated:
            activated = 1
        else:
            activated = 2

        await self.send(
            Message(MGMSG.MOD_SET_CHANENABLESTATE, param1=1, param2=activated)
        )

    async def get_channel_enable_state(self):
        get_msg = await self.send_request(
            MGMSG.MOD_REQ_CHANENABLESTATE, [MGMSG.MOD_GET_CHANENABLESTATE], 1
        )
        self.chan_enabled = get_msg.param2
        if self.chan_enabled == 1:
            self.chan_enabled = True
        elif self.chan_enabled == 2:
            self.chan_enabled = False
        else:
            raise MsgError(
                "Channel state response is invalid: neither "
                "1 nor 2: {}".format(self.chan_enabled)
            )
        return self.chan_enabled

    async def module_identify(self):
        """Ask device to flash its front panel led.

        Instruct hardware unit to identify itself by flashing its front panel
        led.
        """
        await self.send(Message(MGMSG.MOD_IDENTIFY))

    async def hardware_start_update_messages(self, update_rate):
        """Start status updates from the embedded controller.

        Status update messages contain information about the position and
        status of the controller.

        :param update_rate: Rate at which you will receive status updates
        """
        await self.send(Message(MGMSG.HW_START_UPDATEMSGS, param1=update_rate))

    async def hardware_stop_update_messages(self):
        """Stop status updates from the controller."""
        await self.send(Message(MGMSG.HW_STOP_UPDATEMSGS))

    async def hardware_request_information(self):
        return await self.send_request(MGMSG.HW_REQ_INFO, [MGMSG.HW_GET_INFO])

    def is_channel_enabled(self):
        return self.chan_enabled

    async def ping(self):
        try:
            await self.hardware_request_information()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.warning("ping failed", exc_info=True)
            return False
        return True
