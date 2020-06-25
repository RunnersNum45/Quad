from leg import Leg
from servos import Servos
from time import sleep
from parser import Config

class Quad:
	def __init__(self, config_file):
		self.config = Config()
		self.config.read_config(config_file)
		self.servos = Servos(16, self.config.mimimum_pulse, self.config.maximum_pulse, self.config.kill_angle)

		legs = []
		for i in range(4):
			leg = Leg(i, )
			leg.servos(*(self.servos.servo[x] for x in leg_pins[i]))
			leg.offsets(*offsets[i])
			leg.limbs(*lengths)
			legs.append(leg)
		self.leg0, self.leg1, self.leg2, self.leg3 = legs

	def __getitem__(self, index):
		return self.legs[index]

	@property
	def legs(self):
		return (self.leg0, self.leg1, self.leg2, self.leg3)

if __name__ == '__main__':
	q = Quad("config.quad")
	q[0].set(150, 150, 150)
	sleep(3)
	q[0].set(150, 100, -150)
	sleep(3)