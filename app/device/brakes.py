from app.utils.servo import Servo

SERVO_PIN = 18 # physical pin 12

class Brakes(object):
    def __init__(self):
        self.percentage = 0
        self.servo = Servo(SERVO_PIN)
        self.servo.write(0)

    def deploy(self, percentage):
        self.percentage = percentage
        # TODO better conversion from area exposed to servo angle
        servo_position = percentage * 180
        self.servo.write(servo_position)
