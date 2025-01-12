import struct as st

from thorlabs_cube.driver.message import MGMSG, Message
from thorlabs_cube.driver.tcube.tsc import Tsc, TscSim


class Ksc(Tsc):
    """
    KSC101 K-Cube Solenoid Controller class
    """

    async def set_kcubemmi_params(
        self,
        js_mode: int,
        js_max_vel: int,
        js_accn: int,
        dir_sense: int,
        preset_pos1: int,
        preset_pos2: int,
        preset_pos3: int,
        disp_brightness: int,
        disp_timeout: int,
        disp_dim_level: int,
        js_sensitivity: int,
    ) -> None:
        """Set the KCube MMI (joystick) parameters.

        :param js_mode: Joystick mode (1 = velocity control, 2 = jog mode, 3 = go-to-position mode).
        :param js_max_vel: Maximum velocity for the joystick.
        :param js_accn: Acceleration for the joystick.
        :param dir_sense: Direction sense (normal or reversed).
        :param preset_pos1: Preset position 1.
        :param preset_pos2: Preset position 2.
        :param preset_pos3: Preset position 3.
        :param disp_brightness: Display brightness.
        :param disp_timeout: Display timeout in ms.
        :param disp_dim_level: Display dim level.
        :param js_sensitivity: Joystick sensitivity.
        """
        payload = st.pack(
            "<HHLLLHHLLLLH",
            Ksc._CHANNEL,
            js_mode,
            js_max_vel,
            js_accn,
            dir_sense,
            preset_pos1,
            preset_pos2,
            preset_pos3,
            disp_brightness,
            disp_timeout,
            disp_dim_level,
            js_sensitivity,
        )
        await self.send(Message(MGMSG.MOT_SET_KCUBEMMIPARAMS, data=payload))

    async def get_kcubemmi_params(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int, int]:
        """Get the KCube MMI (joystick) parameters.

        :return: A tuple containing the joystick mode, max velocity,
        acceleration, direction sense, preset positions, display
        settings, and joystick sensitivity.
        """
        payload = st.pack("<H", Ksc._CHANNEL)
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_KCUBEMMIPARAMS, [MGMSG.MOT_GET_KCUBEMMIPARAMS], data=payload
        )

        return st.unpack("<HLLLHHLLLLH", get_msg.data[2:])

    async def set_kcubetrigio_config(
        self, trig1_mode: int, trig1_polarity: int, trig2_mode: int, trig2_polarity: int
    ) -> None:
        """Set the KCube trigger I/O configuration parameters.

        :param trig1_mode: Mode for Trigger 1 (input/output).
        :param trig1_polarity: Polarity for Trigger 1 (high/low).
        :param trig2_mode: Mode for Trigger 2 (input/output).
        :param trig2_polarity: Polarity for Trigger 2 (high/low).
        """
        payload = st.pack(
            "<HBBBB",
            Ksc._CHANNEL,
            trig1_mode,
            trig1_polarity,
            trig2_mode,
            trig2_polarity,
        )

        await self.send(Message(MGMSG.MOT_SET_KCUBETRIGIOCONFIG, data=payload))

    async def get_kcubetrigio_config(self) -> tuple[int, int, int, int]:
        """Get the KCube trigger I/O configuration parameters.

        :return: A tuple containing the operating mode, and active state for
        both Trigger 1 and Trigger 2. The active states can assume a High or Low
        whereas, the operating modes can be both input and output respectively

        Input State Operating Modes:

            0x00 The trigger IO is disabled

            0x01 General purpose logic input (read through status bits using the
            MOT_GET_STATUSBITS message).

            0x02 Input trigger for relative move.

            0x03 Input trigger for absolute move.

            0x04 Input trigger for home move.

        Output State Operating Modes:

            0x0A General purpose logic output (set using the MOD_SET_DIGOUTPUTS message).

            0x0B Trigger output active (level) when motor 'in motion'. The output trigger goes high (5V)
            or low (0V) (as set in the lTrig1Polarity and lTrig2Polarity parameters) when the stage is in
            motion.

            0x0C Trigger output active (level) when motor at 'max velocity'.

            0x0D Trigger output active (pulsed) at pre-defined positions moving forward (set using
            StartPosFwd, IntervalFwd, NumPulsesFwd and PulseWidth parameters in the
            SetKCubePosTrigParams message). Only one Trigger port at a time can be set to this mode.

            0x0E Trigger output active (pulsed) at pre-defined positions moving backwards (set using
            StartPosRev, IntervalRev, NumPulsesRev and PulseWidth parameters in the
            SetKCubePosTrigParams message). Only one Trigger port at a time can be set to this mode.

            0x0F Trigger output active (pulsed) at pre-defined positions moving forwards and
            backward. Only one Trigger port at a time can be set to this mode.
        """
        payload = st.pack("<H", Ksc._CHANNEL)
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_KCUBETRIGIOCONFIG,
            [MGMSG.MOT_GET_KCUBETRIGIOCONFIG],
            data=payload,
        )

        return st.unpack("<BBBB", get_msg.data[2:])

    async def set_kcubepostrig_params(
        self,
        start_pos_fwd: int,
        interval_fwd: int,
        num_pulses_fwd: int,
        start_pos_rev: int,
        interval_rev: int,
        num_pulses_rev: int,
        pulse_width: int,
        num_cycles: int,
    ) -> None:
        """Set the KCube post-trigger parameters.

        :param start_pos_fwd: Stage position to start the forward trigger sequence.
        :param interval_fwd: Interval in encoder counts/microsteps for forward trigger pulses.
        :param num_pulses_fwd: Number of output pulses during forward move.
        :param start_pos_rev: Stage position to start the reverse trigger sequence.
        :param interval_rev: Interval in encoder counts/microsteps for reverse trigger pulses.
        :param num_pulses_rev: Number of output pulses during reverse move.
        :param pulse_width: Trigger output pulse width (from 1 μs to 1,000,000 μs).
        :param num_cycles: Number of forward/reverse cycles.
        """
        payload = st.pack(
            "<HLLLLLLLL",
            Ksc._CHANNEL,
            start_pos_fwd,
            interval_fwd,
            num_pulses_fwd,
            start_pos_rev,
            interval_rev,
            num_pulses_rev,
            pulse_width,
            num_cycles,
        )
        await self.send(Message(MGMSG.MOT_SET_KCUBEPOSTRIGPARAMS, data=payload))

    async def get_kcubepostrig_params(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int]:
        """Get the KCube post-trigger parameters.

        :return: A tuple containing (start_pos_fwd, interval_fwd,
        num_pulses_fwd, start_pos_rev, interval_rev, num_pulses_rev,
        pulse_width, num_cycles).
        """
        payload = st.pack("<H", Ksc._CHANNEL)
        get_msg = await self.send_request(
            MGMSG.MOT_REQ_KCUBEPOSTRIGPARAMS,
            [MGMSG.MOT_GET_KCUBEPOSTRIGPARAMS],
            data=payload,
        )

        return st.unpack("<LLLLLLLL", get_msg.data[2:])


class KscSim(TscSim):
    def set_kcubemmi_params(
        self,
        js_mode: int,
        js_max_vel: int,
        js_accn: int,
        dir_sense: int,
        preset_pos1: int,
        preset_pos2: int,
        preset_pos3: int,
        disp_brightness: int,
        disp_timeout: int,
        disp_dim_level: int,
        js_sensitivity: int,
    ) -> None:
        self.js_mode = js_mode
        self.js_max_vel = js_max_vel
        self.js_accn = js_accn
        self.dir_sense = dir_sense
        self.preset_pos1 = preset_pos1
        self.preset_pos2 = preset_pos2
        self.preset_pos3 = preset_pos3
        self.disp_brightness = disp_brightness
        self.disp_timeout = disp_timeout
        self.disp_dim_level = disp_dim_level
        self.js_sensitivity = js_sensitivity

    def get_kcubemmi_params(
        self,
    ) -> tuple[int, int, int, int, int, int, int, int, int, int, int]:
        return (
            self.js_mode,
            self.js_max_vel,
            self.js_accn,
            self.dir_sense,
            self.preset_pos1,
            self.preset_pos2,
            self.preset_pos3,
            self.disp_brightness,
            self.disp_timeout,
            self.disp_dim_level,
            self.js_sensitivity,
        )

    def set_kcubetrigio_config(
        self,
        trig1_mode: int,
        trig1_polarity: int,
        trig2_mode: int,
        trig2_polarity: int,
    ) -> None:
        self.trig1_mode = trig1_mode
        self.trig1_polarity = trig1_polarity
        self.trig2_mode = trig2_mode
        self.trig2_polarity = trig2_polarity

    def get_kcubetrigio_config(self) -> tuple[int, int, int, int]:
        return (
            self.trig1_mode,
            self.trig1_polarity,
            self.trig2_mode,
            self.trig2_polarity,
        )

    def set_kcubepostrig_params(
        self,
        start_pos_fwd: int,
        interval_fwd: int,
        num_pulses_fwd: int,
        start_pos_rev: int,
        interval_rev: int,
        num_pulses_rev: int,
        pulse_width: int,
        num_cycles: int,
    ) -> None:
        self.start_pos_fwd = start_pos_fwd
        self.interval_fwd = interval_fwd
        self.num_pulses_fwd = num_pulses_fwd
        self.start_pos_rev = start_pos_rev
        self.interval_rev = interval_rev
        self.num_pulses_rev = num_pulses_rev
        self.pulse_width = pulse_width
        self.num_cycles = num_cycles

    def get_kcubepostrig_params(self) -> tuple[int, int, int, int, int, int, int, int]:
        return (
            self.start_pos_fwd,
            self.interval_fwd,
            self.num_pulses_fwd,
            self.start_pos_rev,
            self.interval_rev,
            self.num_pulses_rev,
            self.pulse_width,
            self.num_cycles,
        )
