import Adafruit_BBIO.UART as UART
from time import sleep
import serial

class GPS(object):
    def __init__(self):
        UART.setup("UART1")
        self.ser = serial.Serial(port = '/dev/ttyO1', baudrate=9600)
        self.set_baud_rate(57600)
        self.set_data_rate(0.2)
        self.set_datatype("GPRMC_GPGGA")

        sleep(1)
        self.ser.flushInput()
        print "GPS Initialized"

    def read(self):
        print "Starting read"
        self.ser.flushInput()

        data1 = self.ser.readline().split(',')
        data2 = self.ser.readline().split(',')

        if data1[0] == "$GPRMC":
            raw_data["GPRMC"] = data1[1:]
            raw_data["GPGGA"] = data2[1:]
        else:
            raw_data["GPRMC"] = data2[1:]
            raw_data["GPGGA"] = data1[1:]

        return parse_raw_data(raw_data)

    def set_data_rate(self, rate):
        UPDATE_RATE_MAPPINGS = {
            10: "$PMTK220,10000*2F\r\n",
            5: "$PMTK220,5000*1B\r\n",
            1: "$PMTK220,1000*1F\r\n",
            0.2: "$PMTK220,200*2C\r\n",
        }
        MEASURE_RATE_MAPPINGS = {
            10: "$PMTK300,10000,0,0,0,0*2C\r\n",
            5: "$PMTK300,5000,0,0,0,0*18\r\n",
            1: "$PMTK300,1000,0,0,0,0*1C\r\n",
            0.2: "$PMTK300,200,0,0,0,0*2F\r\n",
        }
        if rate not in UPDATE_RATE_MAPPINGS and MEASURE_RATE_MAPPINGS:
            print "WARNING: %s is not a valid datarate" % rate

        self.ser.write(UPDATE_RATE_MAPPINGS[rate])
        #sleep(1)
        self.ser.write(MEASURE_RATE_MAPPINGS[rate])

    def set_baud_rate(self, rate):
        BAUD_RATE_MAPPINGS = {
            9600: '$PMTK251,9600*17\r\n',
            57600: '$PMTK251,57600*2C\r\n',
        }
        if rate not in BAUD_RATE_MAPPINGS:
            print "WARNING: %s is not a valid baud rate" % rate

        self.ser.write(BAUD_RATE_MAPPINGS[rate])
        sleep(1)
        self.ser.baudrate = rate
        self.ser.timeout = 2 * rate

    def set_datatype(self, datatype):
        DATATYPE_MAPPINGS = {
            "GPRMC_GPGGA": "$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n",
            "GPRMC": "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n",
            "None": "$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n",
            "All": "$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n",
        }
        if datatype not in DATATYPE_MAPPINGS:
            print "WARNING: %s is not a valid datatype" % datatype

        self.ser.write(DATATYPE_MAPPINGS[datatype])

    @classmethod
    def parse_raw_data(raw_data):
        data = {}
        data['fix'] = int(raw_data["GPGGA"][5])
        data['sats'] = raw_data["GPGGA"][6]

        if not raw_data["fix"]:
            return data

        data['altitude'] = float(raw_data["GPGGA"][8]) # meters
        data['time']= 1000 * ( int(raw_data['GPRMC'][8][0:2])*86400 + # milliseconds
                               int(raw_data['GPRMC'][0][0:2])*3600 +
                               int(raw_data['GPRMC'][0][2:4])*60 +
                               float(raw_data['GPRMC'][0][4:])
                             )
        data['latitude'] = raw_data['GPRMC'][2] + raw_data['GPRMC'][3]
        data['longitude'] = raw_data['GPRMC'][4] + raw_data['GPRMC'][5]
        data['ground_speed'] = raw_data['GPRMC'][6] # knots
        return data

if __name__ == '__main__':
    gps = GPS()
    while 1:
        print gps.read()
