import pandas as pd
import numpy as np
import datetime


## LOOP METHOD
def get_label(Price):
    windowSize = 11

    maxIndex = 0
    minIndex = 0
    action = []
    counterRow = 0
    len_time = len(Price)
    
    while counterRow<len_time:
        counterRow+=1

        if counterRow>windowSize-1:
            windowBeginIndex = counterRow - windowSize 
            windowEndIndex = windowBeginIndex + windowSize - 1
            windowMiddleIndex = (windowBeginIndex + windowEndIndex)/2
            rangeWindow = np.arange(windowBeginIndex, windowEndIndex+1)
            min_ = 30000
            max_ = 0
            for i in rangeWindow:
                number = Price[i]
                if number<min_:
                    min_ = number
                    minIndex = np.where(Price[rangeWindow]==min_)[0][0]+windowBeginIndex
                if number>max_:
                    max_ = number
                    maxIndex = np.where(Price[rangeWindow]==max_)[0][0]+windowBeginIndex

            if maxIndex == windowMiddleIndex:
                action.append(1)
            elif minIndex == windowMiddleIndex:
                action.append(2)
            else:
                action.append(0)

    return np.asarray(action)

## PYTHONIC VERSION
def get_peak(func):
    def algo(data, window):
        max_local = func(data, window)
        max_local = np.asarray(max_local)
        max_local_valid = np.where(max_local==int(window/2))[0]
        return max_local_valid
    return algo
    
@get_peak
def get_max_peak(data, window):
    return data.rolling(window, center=True).apply(lambda x: np.where(x==np.max(x))[0][0], raw=True)

@get_peak
def get_min_peak(data, window):
    return data.rolling(window, center=True).apply(lambda x: np.where(x==np.min(x))[0][0], raw=True)

def return_min_max_peak(data, window=14):
    i_x = get_max_peak(data['close'], window) #i_x stands for Index_maX
    i_n = get_min_peak(data['close'], window) #i_n stands for Index_miN
    return (i_x,i_n)
      