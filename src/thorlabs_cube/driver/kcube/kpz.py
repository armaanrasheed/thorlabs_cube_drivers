import struct as st

from thorlabs_cube.driver.message import MGMSG, Message
from thorlabs_cube.driver.tcube.tpz import Tpz, TpzSim


class Kpz(Tpz):

    async def set_kcubemmi_params(
        self,
        js_mode: int,
        js_volt_gearbox: int,
        js_volt_step: int,
        dir_sense: int,
        preset_volt1: int,
        preset_volt2: int,
        disp_brightness: int,
        disp_timeout: int,
        disp_dim_level: int,
    ) -> None:
        """Set the KCube MMI parameters.

        :param js_mode: The mode of joystick (JSMODE).
        :param js_volt_gearbox: The rate of change of voltage for the joystick.
        :param js_volt_step: The voltage step size when JSMODE is jog mode.
        :param dir_sense: The direction of joystick motion.
        :param preset_volt1: Preset voltage 1 for "Go To" mode.
        :param preset_volt2: Preset voltage 2 for "Go To" mode.
        :param disp_brightness: The brightness of the display.
        :param disp_timeout: The timeout for display dimming.
        :param disp_dim_level: The dimming level for the display.
        """
        payload = st.pack(
            "<HHHLHLLHHHHHHH",
            Kpz._CHANNEL,
            js_mode,
            js_volt_gearbox,
            js_volt_step,
            dir_sense,
            preset_volt1,
            preset_volt2,
            disp_brightness,
            disp_timeout,
            disp_dim_level,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
        )
        await self.send(Message(MGMSG.KPZ_SET_KCUBEMMIPARAMS, data=payload))

    async def get_kcubemmi_params(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int, int, int, int]:
        """Get the KCube MMI parameters.

        :return: A tuple containing the KCube MMI parameters such as joystick mode,
        voltage gearbox, voltage step, direction sense, preset voltages, display
        brightness, timeout, and dim level. Purpose descriptions found in set_kcubemmi_params()
        """
        get_msg = await self.send_request(
            MGMSG.KPZ_REQ_KCUBEMMIPARAMS, [MGMSG.KPZ_GET_KCUBEMMIPARAMS], Kpz._CHANNEL
        )

        return st.unpack("<HHHLHLLHHHHHHH", get_msg.data[6:])

    async def set_trigio_config(
        self, trig1_mode: int, trig1_polarity: int, trig2_mode: int, trig2_polarity: int
    ) -> None:
        """Set the TRIG1 and TRIG2 input/output configuration.

        :param trig1_mode: The mode of TRIG1.
        :param trig1_polarity: The polarity of TRIG1.
        :param trig2_mode: The mode of TRIG2.
        :param trig2_polarity: The polarity of TRIG2.
        """
        payload = st.pack(
            "<HHHHHHHHHHH",
            Kpz._CHANNEL,
            trig1_mode,
            trig1_polarity,
            trig2_mode,
            trig2_polarity,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
        )
        await self.send(Message(MGMSG.KPZ_SET_KCUBETRIGIOCONFIG, data=payload))

    async def get_trigio_config(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int, int]:
        """Get the TRIG1 and TRIG2 input/output configuration.

        :return: A tuple containing the Trigger IO
        configuration parameters for TRIG1 and TRIG2 (mode, polarity).
        Purpose description can be found in set_trigio_config()
        """
        get_msg = await self.send_request(
            MGMSG.KPZ_REQ_KCUBETRIGIOCONFIG,
            [MGMSG.KPZ_GET_KCUBETRIGIOCONFIG],
            Kpz._CHANNEL,
        )
        return st.unpack("<HHHHHHHHHHH", get_msg.data[6:])


class KpzSim(TpzSim):

    def set_kcubemmi_params(
        self,
        js_mode: int,
        js_volt_gearbox: int,
        js_volt_step: int,
        dir_sense: int,
        preset_volt1: int,
        preset_volt2: int,
        disp_brightness: int,
        disp_timeout: int,
        disp_dim_level: int,
    ) -> None:
        """Set the KCube MMI parameters in simulation.

        This simulates setting the parameters for the joystick, voltages, and display.
        """
        self.js_mode = js_mode
        self.js_volt_gearbox = js_volt_gearbox
        self.js_volt_step = js_volt_step
        self.dir_sense = dir_sense
        self.preset_volt1 = preset_volt1
        self.preset_volt2 = preset_volt2
        self.disp_brightness = disp_brightness
        self.disp_timeout = disp_timeout
        self.disp_dim_level = disp_dim_level

    def get_kcubemmi_params(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int, int, int, int]:
        """Get the KCube MMI parameters in simulation.

        This returns the simulated parameters for the joystick, voltages, and display.
        """
        return (
            self.js_mode,
            self.js_volt_gearbox,
            self.js_volt_step,
            self.dir_sense,
            self.preset_volt1,
            self.preset_volt2,
            self.disp_brightness,
            self.disp_timeout,
            self.disp_dim_level,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
        )

    def set_trigio_config(
        self, trig1_mode: int, trig1_polarity: int, trig2_mode: int, trig2_polarity: int
    ) -> None:
        """Set the TRIG1 and TRIG2 configuration in simulation.

        This simulates setting the TRIG1 and TRIG2 modes and polarities.
        """
        self.trig1_mode = trig1_mode
        self.trig1_polarity = trig1_polarity
        self.trig2_mode = trig2_mode
        self.trig2_polarity = trig2_polarity

    def get_trigio_config(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int]:
        """Get the TRIG1 and TRIG2 configuration in simulation.

        This returns the simulated configuration for the TRIG1 and TRIG2 modes and polarities.
        """
        return (
            self.trig1_mode,
            self.trig1_polarity,
            self.trig2_mode,
            self.trig2_polarity,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
            Kpz._RESERVED,
        )
