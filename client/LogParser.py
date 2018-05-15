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

    def getXs(self,log_file, param):
        param_pattern = '(?<=('+param+' )).*'
        value_pattern = r'(?<=x: )(-?\d*\.?\d*)'

        parse_file = open(log_file, 'r')

        x_data = []
        for line in parse_file:
            match = re.search(param_pattern, line)
            if(match):
                x = re.search(value_pattern, match.group()).group()
                time = self.getTime(line)
                x_data.append([x, time])
        return pd.DataFrame(x_data, columns=['X '+param, 'Time'])

    def getYs(self,log_file, param):
        param_pattern = '(?<=('+param+' )).*'
        value_pattern = r'(?<=y: )(-?\d*\.?\d*)'

        parse_file = open(log_file, 'r')

        y_data = []
        for line in parse_file:
                match = re.search(param_pattern, line)
                if(match):
                    time = self.getTime(line)
                    y = re.search(value_pattern, match.group()).group()
                    y_data.append((time, y))

        return pd.DataFrame(y_data, columns=["Time", 'Y ' + param])

    def getZs(self,log_file, param):
        param_pattern = '(?<=('+param+' )).*'
        value_pattern = r'(?<=z: )(-?\d*\.?\d*)'

        parse_file = open(log_file, 'r')

        z_data = []
        for line in parse_file:
            time = self.getTime(line)
            match = re.search(param_pattern, line)
            if(match):
                z = re.search(value_pattern, match.group()).group()
                z_data.append((time, z))


        return pd.DataFrame(z_data, columns=['Time', 'Z ' + param])
