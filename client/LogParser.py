import re
import numpy as np
import pandas as pd
from datetime import datetime

class LogParser(object):
    POSITION = r'Position'
    VELOCITY = r'Velocity'
    ACCELERATION = r'Acceleration'

    def getTime(self, line):
        pattern = r'[0-9]*\/[0-9]*\/[0-9]* [0-9]*:[0-9]*:[0-9]*?\.[0-9]*'
        t_str = re.search(pattern, line).group()
        if(t_str):
            t = datetime.strptime(t_str, '%m/%d/%Y %H:%M:%S.%f')
            return t
        else:
            return "Error"

    def getErrors(self,log_file):
        print("To implement")

    def getWarnings(self,log_file):
        print("To implement")

    def getData(self, log_file, plane, param):
        param_pattern = '(?<=('+param+' )).*'
        value_pattern = r'(?<=' + plane + r': )(-?\d*\.?\d*)'

        parse_file = open(log_file, 'r')

        data = []
        for line in parse_file:
            match = re.search(param_pattern, line)
            if(match):
                d = re.search(value_pattern, match.group()).group()
                time = self.getTime(line)
                data.append([time, d])
        df = pd.DataFrame(data, columns=['Time', plane + ' ' + param])
        df = df.set_index('Time')
        df = df.astype(float)
        return df

    def getXs(self,log_file, param):
        return self.getData(log_file, 'x', param)

    def getYs(self,log_file, param):
        return self.getData(log_file, 'y', param)

    def getZs(self,log_file, param):
        return self.getData(log_file, 'z', param)
