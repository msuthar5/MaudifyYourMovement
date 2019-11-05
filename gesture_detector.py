import numpy as np
class GestureDetector:
    def __init__(self):
        self.value = 1
    
    def detect(self, state):

        zs = [d['accel_z'] for d in state]
        if len(zs) < 1:
            return False
        if abs(zs[0]) < 0.15:
            return True
        
        