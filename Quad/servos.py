from adafruit_servokit import ServoKit

class Servos:
	def __init__(self, num=16, mimimum_pulse=450, maximum_pulse=2450, kill_angle=90):
		self.kill_angle = kill_angle
		self.kit = ServoKit(channels=16)
		self.servos = [Servo(self.kit.servo[x], x) for x in range(16)]
		for servo in self.servos:
			servo.kit_servo.set_pulse_width_range(mimimum_pulse, maximum_pulse)

	def set(self, angle):
		for servo in self.servos:
			servo.angle = angle

	def __iter__(self):
		return self.servos.__iter__()

	def __getitem__(self, index):
		return self.servos[index]

	def __del__(self):
		self.set(self.kill_angle)

class Servo:
	def __init__(self, kit_servo, num):
		self.kit_servo = kit_servo
		self.num = num
		self._angle = None

	@property
	def angle(self):
		if self._angle is None:
			raise Exception("Servo angle requested before being set, servo {}".format(self.num))
		return self._angle

	@angle.setter
	def angle(self, new_angle):
		self._angle = new_angle
		self.kit_servo.angle = self._angle