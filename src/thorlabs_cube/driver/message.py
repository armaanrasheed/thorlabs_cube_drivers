import struct as st
from enum import Enum


class MGMSG(Enum):
    HW_DISCONNECT = 0x0002
    HW_REQ_INFO = 0x0005
    HW_GET_INFO = 0x0006
    HW_START_UPDATEMSGS = 0x0011
    HW_STOP_UPDATEMSGS = 0x0012
    HUB_REQ_BAYUSED = 0x0065
    HUB_GET_BAYUSED = 0x0066
    HW_RESPONSE = 0x0080
    HW_RICHRESPONSE = 0x0081
    MOD_SET_CHANENABLESTATE = 0x0210
    MOD_REQ_CHANENABLESTATE = 0x0211
    MOD_GET_CHANENABLESTATE = 0x0212
    MOD_SET_DIGOUTPUTS = 0x0213
    MOD_REQ_DIGOUTPUTS = 0x0214
    MOD_GET_DIGOUTPUTS = 0x0215
    MOD_IDENTIFY = 0x0223
    MOT_SET_ENCCOUNTER = 0x0409
    MOT_REQ_ENCCOUNTER = 0x040A
    MOT_GET_ENCCOUNTER = 0x040B
    MOT_SET_POSCOUNTER = 0x0410
    MOT_REQ_POSCOUNTER = 0x0411
    MOT_GET_POSCOUNTER = 0x0412
    MOT_SET_VELPARAMS = 0x0413
    MOT_REQ_VELPARAMS = 0x0414
    MOT_GET_VELPARAMS = 0x0415
    MOT_SET_JOGPARAMS = 0x0416
    MOT_REQ_JOGPARAMS = 0x0417
    MOT_GET_JOGPARAMS = 0x0418
    MOT_SET_LIMSWITCHPARAMS = 0x0423
    MOT_REQ_LIMSWITCHPARAMS = 0x0424
    MOT_GET_LIMSWITCHPARAMS = 0x0425
    MOT_REQ_STATUSBITS = 0x0429
    MOT_GET_STATUSBITS = 0x042A
    MOT_GET_STATUSUPDATE = 0x0481
    MOT_REQ_STATUSUPDATE = 0x0480
    MOT_SET_GENMOVEPARAMS = 0x043A
    MOT_REQ_GENMOVEPARAMS = 0x043B
    MOT_GET_GENMOVEPARAMS = 0x043C
    MOT_SET_HOMEPARAMS = 0x0440
    MOT_REQ_HOMEPARAMS = 0x0441
    MOT_GET_HOMEPARAMS = 0x0442
    MOT_MOVE_HOME = 0x0443
    MOT_MOVE_HOMED = 0x0444
    MOT_SET_MOVERELPARAMS = 0x0445
    MOT_REQ_MOVERELPARAMS = 0x0446
    MOT_GET_MOVERELPARAMS = 0x0447
    MOT_MOVE_RELATIVE = 0x0448
    MOT_SET_MOVEABSPARAMS = 0x0450
    MOT_REQ_MOVEABSPARAMS = 0x0451
    MOT_GET_MOVEABSPARAMS = 0x0452
    MOT_MOVE_ABSOLUTE = 0x0453
    MOT_MOVE_VELOCITY = 0x0457
    MOT_MOVE_COMPLETED = 0x0464
    MOT_MOVE_STOP = 0x0465
    MOT_MOVE_STOPPED = 0x0466
    MOT_MOVE_JOG = 0x046A
    MOT_SUSPEND_ENDOFMOVEMSGS = 0x046B
    MOT_RESUME_ENDOFMOVEMSGS = 0x046C
    MOT_REQ_DCSTATUSUPDATE = 0x0490
    MOT_GET_DCSTATUSUPDATE = 0x0491
    MOT_ACK_DCSTATUSUPDATE = 0x0492
    MOT_SET_DCPIDPARAMS = 0x04A0
    MOT_REQ_DCPIDPARAMS = 0x04A1
    MOT_GET_DCPIDPARAMS = 0x04A2
    MOT_SET_POTPARAMS = 0x04B0
    MOT_REQ_POTPARAMS = 0x04B1
    MOT_GET_POTPARAMS = 0x04B2
    MOT_SET_AVMODES = 0x04B3
    MOT_REQ_AVMODES = 0x04B4
    MOT_GET_AVMODES = 0x04B5
    MOT_SET_BUTTONPARAMS = 0x04B6
    MOT_REQ_BUTTONPARAMS = 0x04B7
    MOT_GET_BUTTONPARAMS = 0x04B8
    MOT_SET_EEPROMPARAMS = 0x04B9
    MOT_SET_KCUBEMMIPARAMS = 0x0520
    MOT_REQ_KCUBEMMIPARAMS = 0x0521
    MOT_GET_KCUBEMMIPARAMS = 0x0522
    MOT_SET_KCUBETRIGIOCONFIG = 0x0523
    MOT_REQ_KCUBETRIGIOCONFIG = 0x0524
    MOT_GET_KCUBETRIGIOCONFIG = 0x0525
    MOT_SET_KCUBEPOSTRIGPARAMS = 0x0526
    MOT_REQ_KCUBEPOSTRIGPARAMS = 0x0527
    MOT_GET_KCUBEPOSTRIGPARAMS = 0x0528
    MOT_SET_SOL_OPERATINGMODE = 0x04C0
    MOT_REQ_SOL_OPERATINGMODE = 0x04C1
    MOT_GET_SOL_OPERATINGMODE = 0x04C2
    MOT_SET_SOL_CYCLEPARAMS = 0x04C3
    MOT_REQ_SOL_CYCLEPARAMS = 0x04C4
    MOT_GET_SOL_CYCLEPARAMS = 0x04C5
    MOT_SET_SOL_INTERLOCKMODE = 0x04C6
    MOT_REQ_SOL_INTERLOCKMODE = 0x04C7
    MOT_GET_SOL_INTERLOCKMODE = 0x04C8
    MOT_SET_SOL_STATE = 0x04CB
    MOT_REQ_SOL_STATE = 0x04CC
    MOT_GET_SOL_STATE = 0x04CD
    PZ_SET_POSCONTROLMODE = 0x0640
    PZ_REQ_POSCONTROLMODE = 0x0641
    PZ_GET_POSCONTROLMODE = 0x0642
    PZ_SET_OUTPUTVOLTS = 0x0643
    PZ_REQ_OUTPUTVOLTS = 0x0644
    PZ_GET_OUTPUTVOLTS = 0x0645
    PZ_SET_OUTPUTPOS = 0x0646
    PZ_REQ_OUTPUTPOS = 0x0647
    PZ_GET_OUTPUTPOS = 0x0648
    PZ_SET_INPUTVOLTSSRC = 0x0652
    PZ_REQ_INPUTVOLTSSRC = 0x0653
    PZ_GET_INPUTVOLTSSRC = 0x0654
    PZ_SET_PICONSTS = 0x0655
    PZ_REQ_PICONSTS = 0x0656
    PZ_GET_PICONSTS = 0x0657
    PZ_GET_PZSTATUSUPDATE = 0x0661
    PZ_SET_OUTPUTLUT = 0x0700
    PZ_REQ_OUTPUTLUT = 0x0701
    PZ_GET_OUTPUTLUT = 0x0702
    PZ_SET_OUTPUTLUTPARAMS = 0x0703
    PZ_REQ_OUTPUTLUTPARAMS = 0x0704
    PZ_GET_OUTPUTLUTPARAMS = 0x0705
    PZ_START_LUTOUTPUT = 0x0706
    PZ_STOP_LUTOUTPUT = 0x0707
    PZ_SET_EEPROMPARAMS = 0x07D0
    PZ_SET_TPZ_DISPSETTINGS = 0x07D1
    PZ_REQ_TPZ_DISPSETTINGS = 0x07D2
    PZ_GET_TPZ_DISPSETTINGS = 0x07D3
    PZ_SET_TPZ_IOSETTINGS = 0x07D4
    PZ_REQ_TPZ_IOSETTINGS = 0x07D5
    PZ_GET_TPZ_IOSETTINGS = 0x07D6
    KPZ_SET_KCUBEMMIPARAMS = 0x07F0
    KPZ_REQ_KCUBEMMIPARAMS = 0x07F1
    KPZ_GET_KCUBEMMIPARAMS = 0x07F2
    KPZ_SET_KCUBETRIGIOCONFIG = 0x07F3
    KPZ_REQ_KCUBETRIGIOCONFIG = 0x07F4
    KPZ_GET_KCUBETRIGIOCONFIG = 0x07F5
    QUAD_SET_PARAMS = 0x0870
    QUAD_REQ_PARAMS = 0x0871
    QUAD_GET_PARAMS = 0x0872
    QUAD_SET_EEPROM_PARAMS = 0x0875
    QUAD_REQ_STATUSUPDATE = 0x0880
    QUAD_GET_STATUSUPDATE = 0x0881
    QUAD_ACK_STATUSUPDATE = 0x0882


class QUADMSG(Enum):
    QUAD_LOOP_PARAMS_SUB_ID: int = 0x1
    QUAD_READINGS_SUB_ID: int = 0x3
    QUAD_POSITION_DEMAND_PARAMS_SUB_ID: int = 0x5
    QUAD_OPER_MODE_SUB_ID: int = 0x7
    QUAD_STATUS_BITS_SUB_ID: int = 0x9
    QUAD_DISP_SETTINGS_SUB_ID: int = 0xB
    QUAD_POSITION_OUTPUTS_SUB_ID: int = 0xD
    QUAD_LOOP_PARAMS_TWO_SUB_ID = 0xE
    QUAD_KPA_TRIGIO_SUB_ID: int = 0x0F
    QUAD_KPA_DIGOPS_SUB_ID: int = 0x10


class Direction:
    def __init__(self, direction):
        if direction not in (1, 2):
            raise ValueError("Direction must be either 1 or 2")
        self.direction = direction

    def __str__(self):
        if self.direction == 1:
            return "forward"
        else:
            return "backward"


class MsgError(Exception):
    pass


class Message:
    def __init__(self, id, param1=0, param2=0, dest=0x50, src=0x01, data=None):
        if data is not None:
            dest |= 0x80
        self.id = id
        self.param1 = param1
        self.param2 = param2
        self.dest = dest
        self.src = src
        self.data = data

    def __str__(self):
        return (
            "<Message {} p1=0x{:02x} p2=0x{:02x} "
            "dest=0x{:02x} src=0x{:02x}>".format(
                self.id, self.param1, self.param2, self.dest, self.src
            )
        )

    @staticmethod
    def unpack(data):
        id, param1, param2, dest, src = st.unpack("<HBBBB", data[:6])
        data = data[6:]
        if dest & 0x80:
            if data and len(data) != param1 | (param2 << 8):
                raise ValueError(
                    "If data are provided, param1 and param2"
                    " should contain the data length"
                )
        else:
            data = None
        return Message(MGMSG(id), param1, param2, dest, src, data)

    def pack(self):
        if self.has_data:
            return (
                st.pack(
                    "<HHBB",
                    self.id.value,
                    len(self.data),
                    self.dest | 0x80,
                    self.src,
                )
                + self.data
            )
        else:
            return st.pack(
                "<HBBBB",
                self.id.value,
                self.param1,
                self.param2,
                self.dest,
                self.src,
            )

    @property
    def has_data(self):
        return self.dest & 0x80

    @property
    def data_size(self):
        if self.has_data:
            return self.param1 | (self.param2 << 8)
        else:
            raise ValueError
