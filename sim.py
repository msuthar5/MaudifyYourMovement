import mym_sim

ROOT = "/home/john/Downloads/gbss_data/data"
OBSERVERS = {
    "gyro": ROOT + "/inplace-sway-dribble-10_Gyroscope.csv",
    "accel": ROOT + "/inplace-sway-dribble-10_Accelerometer.csv"
    }



with mym_sim.MaudifyYourMovementSimulator(OBSERVERS, verbose=True, frequency=12) as m:
    while True:
        pass