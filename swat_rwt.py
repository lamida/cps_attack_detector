import sys
import time

T101_H = 800  # mm
T101_L = 500  # mm
P101 = 1  # ON
MV101 = 0  # OPEN
INFLOW_OPEN_ON = 1.11857  # mm/min
INFLOW_OPEN_OFF = 28.5234  # mm/min
OUTFLOW_CLOSED_ON = 27.40  # mm/min
PLC_SAMPLES = 1000
PLC_PERIOD_SEC = 0.10

count = 0
new_level = 500
while(count <= PLC_SAMPLES):

    new_level = new_level
    #print(str(MV101),str(P101))

    # inflows volumes
    if str(MV101) == "0" and str(P101) == "0":
        break

    elif str(MV101) == "1" and str(P101) == "1":
        new_level += INFLOW_OPEN_ON

    elif str(MV101) == "1" and str(P101) == "0":
        new_level += INFLOW_OPEN_OFF

    else:
        new_level -= OUTFLOW_CLOSED_ON

    # level cannot be negative
    if new_level <= 0.0:
        new_level = 0.0

    # HIGHER from 0.800 m
    if new_level >= T101_H:
        print('DEBUG RawWaterTank T101 above H count: ', count)
        MV101 = 0
        P101 = 1

    # LOWER T 0.500 m
    elif new_level <= T101_L:
        print('DEBUG RawWaterTank T101 below L count: ', count)
        MV101 = 1
        P101 = 0

    elif new_level < T101_H and new_level > T101_L:
        MV101 = 1
        P101 = 1

    count += 1
    print('water level ', new_level, ' @ count ', count)
    time.sleep(PLC_PERIOD_SEC)
