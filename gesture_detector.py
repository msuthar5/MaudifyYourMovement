import numpy as np
class GestureDetector:
    def __init__(self):
        self.value = 1
        self.records=list()
        self.skip=0
    
    def detect(self, state,window_size=8,epsilon=7):

        if len(state)<(window_size-1):
        	return False
        if self.skip > 0:
        	self.skip-=1
        	return False

        state=sorted(state, key = lambda i: i['accel_time'])
        zs = [d['accel_z'] for d in state]
        xs = [d['accel_x'] for d in state]
        times = [d['accel_time'] for d in state]
        coef=np.polyfit(times,xs,2)
        if coef[0] > epsilon:
        	self.skip=window_size-1
        	print("DATA:" + str(xs))
        	return True
        else:
        	return False