from enum import Enum

data_struct = '''
struct Data{
    u32 time;
    f32 power_voltage;
    f32 power_current;
    f32 signal_voltage;
    f32 signal_current;
    f32 target_angle;
    f32 angle;
};
'''



class Cmd(Enum):
    Pop 		= 0
    Clear 		= 1
    Start 		= 2
    Pause 		= 3
    Reset 		= 4
    StopData 	= 5
    StartData 	= 6
    ResetTime	= 7
    To485 		= 8
    SetMaxAngle = 9
    SetOutut	= 10
    ResetAngle  = 11
    SetMaxPwm   = 12
    SetMinPwm   = 13
    # To push
    SetAngle 	= 1024
    Wait 		= 1025
    FreqResp    = 1026
    PowerEnable = 1027
    SignalEnable = 1028
    # Get
    GetMaxAngle = 2048

class Status(Enum):
    Ok				= 0
    InvalidHead		= 1
    InvalidCrc		= 2
    IsFull			= 3
    Done            = 4