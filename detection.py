def isDribble(window,epsilon=12):
    coef=np.polyfit(window["elapsed (s)"],window["x-axis (g)"],2)
    if coef[0] > epsilon:
        #print(window[["elapsed (s)","x-axis (g)"]])
        return coef[0]
    return False

def isShot(window,epsilon=-12):
    coef=np.polyfit(window["elapsed (s)"],window["y-axis (g)"],2)
    if coef[0] < epsilon:
        #print(window[["elapsed (s)","y-axis (g)"]])
        return coef[0]
    return False

def detectMovements(records,windowSize=7):
    skip=0
    for i in range(len(df)-windowSize+1):
        if skip>0:
            skip-=1
            continue
        drib=isDribble(df.iloc[i:i+windowSize])
        shot=isShot(df.iloc[i:i+windowSize])
        if drib and shot:
            if abs(drib)>abs(shot):
                print("DRIBBLE-BOTH",drib,shot)
                skip=windowSize
            else:
                print("JUMP SHOT-BOTH",shot,drib)
                skip=1.5*windowSize
        elif drib:
            print("DRIBBLE",drib)
            skip=windowSize
        elif shot:
            print("JUMP SHOT",shot)
            skip=1.5*windowSize
