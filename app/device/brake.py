from app.utils.servo import Servo
from app.utils.exceptions import InvalidArguments

SERVO_PIN = 18 # physical pin 12

class Brake(object):
    def __init__(self):
        self.percentage = 0
        self.servo = Servo(SERVO_PIN)
        self.servo.write(0)

    def deploy(self, percentage):
        if percentage < 0.0 or percentage > 100.0:
            raise InvalidArguments("percentage must be in range (0, 100)")
        self.percentage = percentage
        # TODO better conversion from area exposed to servo angle
        servo_position = percentage * 1.80
        self.servo.write(servo_position)
