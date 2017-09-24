"""
Example "Arcade" library code.

This example shows the drawing primitives and how they are used.
It does not assume the programmer knows how to define functions or classes
yet.

API documentation for the draw commands can be found here:
https://pythonhosted.org/arcade/arcade.html#module-arcade.draw_commands

A video explaining this example can be found here:
https://vimeo.com/167158158
"""

# Import the Arcade library. If this fails, then try following the instructions
# for how to install arcade:
# https://pythonhosted.org/arcade/installation.html
import arcade
import math
import random
from copy import deepcopy

class simplePoint():

	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "x: " + str(self.x) + " y: " + str(self.y)
		
	def __repr__(self):
		return "x: " + str(self.x) + " y: " + str(self.y)
		
	def convert_to_tuple(self):
		return (self.x, self.y)
		
class slope():
	
	def __init__(self, min, max, mod):
		self.min = min
		self.max = max
		self.mod = mod
		
class mountain():

	def __init__(self, centrePoint, numberOfRings):
		self.centrePoint = centrePoint
		self.numberOfRings = numberOfRings
		self.rings = []
		self.peak = {'minSize' : 10, 'maxSize' : 20, 'numberOfPoints' : 8}
		
	def set_slope_all(self, min, max, mod = 0):
		self.slope_pxpy = slope(min, max, mod)
		self.slope_nxny = slope(min, max, mod)
		self.slope_pxny = slope(min, max, mod)
		self.slope_nxpy = slope(min, max, mod)
		
	def set_slope_pxpy(self, min, max, mod = 0):
		self.slope_pxpy = slope(min, max, mod)
		
	def set_slope_nxny(self, min, max, mod = 0):
		self.slope_nxny = slope(min, max, mod)
		
	def set_slope_pxny(self, min, max, mod = 0):
		self.slope_pxny = slope(min, max, mod)
		
	def set_slope_nxpy(self, min, max, mod = 0):
		self.slope_nxpy = slope(min, max, mod)
	
	def define_peak(self, minSize, maxSize, numberOfPoints):
		self.starting_points = numberOfPoints
		self.peak = {'minSize' : minSize, 'maxSize' : maxSize, 'numberOfPoints' : numberOfPoints}
		
	def generate_slope(self):
		random.seed()
		self.slope = []
		for i in range(self.starting_points):
			self.slope.append(slope(random.uniform(1, 15),random.uniform(10, 30), 0))
			
	def generate_slope2(self):
		random.seed()
		self.slopeMin = random_ift(lambda f: 3, 360)
		self.slopeMax = random_ift(lambda f: 5*f*f, 360)
		self.slopeMin = normalise(self.slopeMin, 1, 15)
		self.slopeMax = normalise(self.slopeMax, 10, 30)
		
	def get_slope2(self, angle):
		#print(str(normalise_angle(angle)))
		rounded = round_to_base(normalise_angle(angle), 360/self.starting_points)
		#print(str(rounded))
		index = int(rounded/(360/self.starting_points))-1
		#print(str(index))
		return self.slope[index]
		
	def get_slope3(self, angle):
		#print(str(normalise_angle(angle)))
		rounded = math.floor(normalise_angle(angle))
		#print(str(self.slope[ring][rounded]))
		return slope(self.slopeMin[rounded], self.slopeMax[rounded], 0)
	
	def get_slope(self, point):
		quadrant = (math.copysign(1, point.x - self.centrePoint.x), math.copysign(1, point.y - self.centrePoint.y))
		if quadrant == (1,1):
			return self.slope_pxpy
		elif quadrant == (-1,-1):
			return self.slope_nxny
		elif quadrant == (1,-1):
			return self.slope_pxny
		elif quadrant == (-1,1):
			return self.slope_nxpy
		
	def generate(self):
		firstRing = generate_starting_points(self.centrePoint, self.peak['minSize'], self.peak['maxSize'], self.peak['numberOfPoints'])
		self.generate_slope2()
		print("First Ring Generated")
		self.rings.append(firstRing)
		previousRing = firstRing
		for i in range(self.numberOfRings):
			ring = []
			for j in range(len(previousRing)):
				p1Inside = True
				count = 0
				while p1Inside:
					#slope = self.get_slope(previousRing[j])
					#point = generate_random_point(self.centrePoint, previousRing[j], slope.min + (slope.mod * i) + count, slope.max + (slope.mod * i) + count, 5)
					point = self.generate_random_point2(self.centrePoint, previousRing[j], 5, count)
					count += 0.05
					p1Inside = point_inside_polygon(point, previousRing)
				if (i % 3 == 0):
					p2Inside = True
					count = 0
					while p2Inside:
						middle = midpoint(previousRing[j], previousRing[j-1])
						#slope = self.get_slope(middle)
						#point2 = generate_random_point(self.centrePoint, middle, slope.min + (slope.mod * i) + count, slope.max + (slope.mod * i) + count, 5)
						point2 = self.generate_random_point2(self.centrePoint, middle, 5, count)
						count += 0.05
						p2Inside = point_inside_polygon(point2, previousRing)
					if (distance_between(point, point2) > 5):
						ring.append(point2)
				ring.append(point)
				#print(str(270 - angle_between(self.centrePoint, point)))
				#arcade.draw_line(previousRing[j].x, previousRing[j].y, point.x, point.y, arcade.color.WOOD_BROWN, 3)
			self.rings.append(ring)
			previousRing = ring
			print("Ring " + str(i) + " generated")
		
	def draw(self):
		for ring in self.rings:
			outputRing = []
			for point in ring:
				outputRing.append(point.convert_to_tuple())
			#arcade.draw_line_strip(outputRing, arcade.color.TROPICAL_RAIN_FOREST, 2)
			arcade.draw_polygon_outline(outputRing, arcade.color.SPANISH_VIOLET, 3)
	
	def generate_random_point2(self, p1, p2, angleRange, adjustment):
		random.seed()
		angleDif = angle_between(p1, p2)
		slope = self.get_slope3(angleDif)
		#dist = random.uniform(slope.min + adjustment, slope.max + adjustment) #Not very smooth, nice irregularity
		#dist = weighted_random(int(slope.min + adjustment), int(slope.max + adjustment)) #A little irregular and unnatural looking
		dist = lowest_roll(int(slope.min + adjustment), int(slope.max + adjustment), 2)  #Quite good
		#dist = min(random.uniform(slope.min + adjustment, slope.max + adjustment), random.uniform(slope.min + adjustment, slope.max + adjustment))  #Smooth, good results
		angle = math.radians(270 - random.uniform(angleDif - angleRange, angleDif + angleRange))
		x = dist * math.sin(angle) + p2.x
		y = dist * math.cos(angle) + p2.y
		return simplePoint(x, y)
		
def noise(freq, size):
	phase = random.uniform(0, 2*math.pi)
	return [math.sin(2*math.pi * freq*x/size + phase)
		for x in range(size)]

def weighted_sum(amplitudes, noises, size):
	output = [0.0] * size
	for k in range(len(noises)):
		for x in range(size):
			output[x] += amplitudes[k] * noises[k][x]
	return output

def random_ift(amplitude, size):
	frequencies = range(1, 31)
	output = []
	random.seed()
	amplitudes = [amplitude(f) for f in frequencies]
	noises = [noise(f, size) for f in frequencies]
	sum_of_noises = weighted_sum(amplitudes, noises, size)
	return sum_of_noises

def round_to_base(x, base=5):
    return int(base * round(float(x)/base))
	
def normalise(numberRange, newMin, newMax):
	oldMin = min(numberRange)
	oldMax = max(numberRange)
	output = []
	for x in numberRange:
		y = (((newMax - newMin) * (x - oldMin)) / (oldMax - oldMin)) + newMin
		output.append(y)
	return output
	
def normalise_angle(angle):
	adjustedAngle = 270 - angle
	if (adjustedAngle >= 360):
		adjustedAngle -= 360
	return adjustedAngle
	
def distance_between(p1, p2):
	x = p2.x - p1.x
	y = p2.y - p1.y
	return math.sqrt(x*x + y*y)

def angle_between(p1, p2):
	dy = p1.y - p2.y
	dx = p1.x - p2.x
	return math.degrees(math.atan2(dy, dx))
	
def midpoint(p1, p2):
	x = (p1.x + p2.x)/2
	y = (p1.y + p2.y)/2
	return simplePoint(x, y)
	
def weighted_random(min, max):
	num = 0
	for i in range(min):
		num += random.uniform(1, max/min)
	return num
	
def lowest_roll(minimum, max, numberOfRolls):
	rolls = []
	for i in range(numberOfRolls):
		roll = weighted_random(minimum, max)
		rolls.append(roll)
	return min(rolls)
	
def point_inside_polygon(point,polygon):

	poly = deepcopy(polygon)
	n = len(poly)
	inside =False

	p1 = poly[0]
	for i in range(n+1):
		p2 = poly[i % n]
		if point.y > min(p1.y,p2.y):
			if point.y <= max(p1.y,p2.y):
				if point.x <= max(p1.x,p2.x):
					if p1.y != p2.y:
						xinters = (point.y-p1.y)*(p2.x-p1.x)/(p2.y-p1.y)+p1.x
					if p1.x == p2.x or point.x <= xinters:
						inside = not inside
		p1.x,p1.y = p2.x,p2.y

	return inside
	
def generate_starting_points(p1, minDist, maxDist, numberOfPoints):
	random.seed()
	angleRange = 360/numberOfPoints
	points = []
	for index in range(numberOfPoints):
		dist = random.uniform(minDist, maxDist)
		angle = math.radians(random.uniform(index * angleRange, (index + 1) * angleRange))
		x = dist * math.sin(angle) + p1.x
		y = dist * math.cos(angle) + p1.y
		points.append(simplePoint(x, y))
	return points
		
def generate_random_point(p1, p2, minDist, maxDist, angleRange):
	random.seed()
	angleDif = angle_between(p1, p2)
	dist = random.uniform(minDist, maxDist)
	angle = math.radians(270 - random.uniform(angleDif - angleRange, angleDif + angleRange))
	x = dist * math.sin(angle) + p2.x
	y = dist * math.cos(angle) + p2.y
	return simplePoint(x, y)
	
def generate_point(p1, p2, dist):
	angleDif = math.radians(270 - angle_between(p1, p2))
	x = dist * math.sin(angleDif) + p1.x
	y = dist * math.cos(angleDif) + p1.y
	return simplePoint(x, y)

# Open the window. Set the window title and dimensions (width and height)
arcade.open_window(600, 600, "Drawing Example")

# Set the background color to white
# For a list of named colors see
# https://pythonhosted.org/arcade/arcade.color.html
# Colors can also be specified in (red, green, blue) format and
# (red, green, blue, alpha) format.
arcade.set_background_color(arcade.color.WHITE)

# Start the render process. This must be done before any drawing commands.
arcade.start_render()

cp = simplePoint(300,300)

aMountain = mountain(cp, 10)
aMountain.define_peak(5, 20, 12)
aMountain.set_slope_pxpy(5, 15)
aMountain.set_slope_pxny(5, 15)
aMountain.set_slope_nxpy(10, 20)
aMountain.set_slope_nxny(10, 20)
aMountain.set_slope_all(5, 20)
aMountain.generate()
aMountain.draw()
# firstRing = generate_starting_points(cp, 30, 40, 8)
# for point in firstRing:
#	arcade.draw_point(point.x, point.y, arcade.color.BLUE, 10)
# newPoint = generate_random_point(cp, simplePoint(195, 265), 20, 40, 45)
# output = "x: " + str(newPoint.x) + " y: " + str(newPoint.y)
# arcade.draw_point(newPoint.x, newPoint.y, arcade.color.RED, 10)
arcade.draw_point(cp.x, cp.y, arcade.color.RED, 10)
# arcade.draw_text(output, 0, 0, arcade.color.BLACK, 12)

# Finish the render.
# Nothing will be drawn without this.
# Must happen after all draw commands
arcade.finish_render()

# Keep the window up until someone closes it.
arcade.run()