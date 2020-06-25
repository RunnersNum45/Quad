from math import asin, acos, atan2, sqrt, degrees

class Leg:
	def __init__(self, quadrant, position):
		self.quadrant = quadrant
		self.offsets = position

		self.x = 0.0
		self.y = 0.0
		self.z = 0.0

	def limbs(self, coxa, femur, tibia):
		self.coxa = coxa
		self.femur = femur
		self.tibia = tibia

	def offsets(self, hip=0, knee=0, ankle=0):
		self.hipoff = hip
		self.kneeoff = knee
		self.ankleoff = ankle

	def servos(self, hip, knee, ankle):
		self.hip = hip
		self.knee = knee
		self.ankle = ankle

	def __len__(self):
		return sqrt(self.x**2+self.y**2+self.z**2)

	@property
	def pos(self):
		return (self.x, self.y, self.z)

	def set(self, x, y, z):
		self.x,	self.y, self.z = (cord-offset for cord, offset in zip((x, y, z), self.offsets))

		f = sqrt(self.x**2+self.y**2)-self.coxa
		d = sqrt(f**2+self.z**2)

		b1 = atan2(self.z, f)
		b2 = acos((self.femur**2+d**2-self.tibia**2)/(2*self.femur*d))

		h = degrees(atan2(self.x, self.y))%360
		k = degrees(b1+b2)%360
		a = degrees(acos((self.femur**2+self.tibia**2-d**2)/(2*self.femur*self.tibia)))%360

		self.hip.angle = (h+self.hipoff)*[1, 1, 1, 1][self.quadrant]
		self.knee.angle = (k+self.kneeoff)*[1, 1, 1, 1][self.quadrant]
		self.ankle.angle = (a+self.ankleoff)*[1, 1, 1, 1][self.quadrant]
