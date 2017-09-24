import pygame
import contour
import simpleGeometry
import simpleNoise
import random
import math

class slope():
	
	def __init__(self, min, max):
		self.min = min
		self.max = max

class contour_group(object):

	def __init__(self, centrePoint, startElevation, scale, depression):
		self.centrePoint = centrePoint
		self.elevation = startElevation
		self.scale = scale
		self.numberOfRings = int(self.elevation / self.scale)
		self.depression = depression
		self.contours = []
		self.displacements = []
		self.startParameters = {'minSize' : 10, 'maxSize' : 20, 'numberOfPoints' : 8}
		
	def define_start(self, minSize, maxSize, numberOfPoints):
		self.starting_points = numberOfPoints
		self.startParameters = {'minSize' : minSize, 'maxSize' : maxSize, 'numberOfPoints' : numberOfPoints}
		
	def define_displacements(self, number, maxRange):
		for i in range(number):
			x = random.uniform(self.centrePoint.x - maxRange/2, self.centrePoint.x + maxRange/2)
			y = random.uniform(self.centrePoint.y - maxRange/2, self.centrePoint.y + maxRange/2)
			point = simpleGeometry.simplePoint(x, y)
			xRadius = random.uniform(0, maxRange/3)
			yRadius = random.uniform(0, maxRange/3)
			angle = random.uniform(0, 359)
			ellipse = simpleGeometry.simpleEllipse(point, xRadius, yRadius, angle)
			self.displacements.append(ellipse)
		
	def generate_starting_points(self):
		params = self.startParameters
		random.seed()
		angleRange = 360/params['numberOfPoints']
		points = []
		for index in range(params['numberOfPoints']):
			dist = random.uniform(params['minSize'], params['maxSize'])
			angle = math.radians(random.uniform(index * angleRange, (index + 1) * angleRange))
			x = dist * math.sin(angle) + self.centrePoint.x
			y = dist * math.cos(angle) + self.centrePoint.y
			points.append(contour.contourPoint(x, y, self.centrePoint))
		poly = contour.contourLine(points, self.elevation)
		return poly
		
	def generate_random_point(self, p1, p2, angleRange, adjustment):
		random.seed()
		angleDif = simpleGeometry.angle_between(p1, p2)
		slope = self.get_slope(angleDif)
		#dist = random.uniform(slope.min + adjustment, slope.max + adjustment) #Not very smooth, nice irregularity
		#dist = simpleNoise.weighted_random(int(slope.min + adjustment), int(slope.max + adjustment)) #A little irregular and unnatural looking
		dist = simpleNoise.lowest_roll(int(slope.min + adjustment), int(slope.max + adjustment), 2)  #Quite good
		#dist = min(random.uniform(slope.min + adjustment, slope.max + adjustment), random.uniform(slope.min + adjustment, slope.max + adjustment))  #Smooth, good results
		angle = math.radians(270 - random.uniform(angleDif - angleRange, angleDif + angleRange))
		x = dist * math.sin(angle) + p2.x
		y = dist * math.cos(angle) + p2.y
		return contour.contourPoint(x, y, p2)
		
	def generate_displaced_point(self, ellipse, p1):
		random.seed()
		angle = math.radians(270 - simpleGeometry.angle_between(ellipse.centre, p1))
		dist =  p1.parentDistance - 1#random.uniform(0, p1.parentDistance - 1)
		x = dist * math.sin(angle) + p1.x
		y = dist * math.cos(angle) + p1.y
		#print ("Original " + str(p1) + " Displaced: " + str(contour.contourPoint(x, y, p1.parent)))
		return contour.contourPoint(x, y, p1.parent)
		
	def check_point(self, point, pointList):
		for p in pointList:
			if (simpleGeometry.distance_between(p, point) < 5):
				return False
		return True
		
	def displace_point(self, point):
		for d in self.displacements:
			if d.point_inside(point):
				return self.generate_displaced_point(d, point)
		return point
		
	def generate_slope(self):
		random.seed()
		self.slopeMin = simpleNoise.random_ift(lambda f: 3, 360)
		self.slopeMax = simpleNoise.random_ift(lambda f: 5*f*f, 360)
		self.slopeMin = simpleGeometry.normalise(self.slopeMin, 2, 10)
		self.slopeMax = simpleGeometry.normalise(self.slopeMax, 10, 30)
		
	def get_slope(self, angle):
		rounded = math.floor(simpleGeometry.normalise_angle(angle))
		return slope(self.slopeMin[rounded], self.slopeMax[rounded])
		
	def generate(self):
		firstRing = self.generate_starting_points()
		self.generate_slope()
		print("First Ring Generated")
		self.contours.append(firstRing)
		previousRing = firstRing
		currentElevation = self.elevation
		for i in range(self.numberOfRings):
			if self.depression:
				currentElevation += self.scale
			else:
				currentElevation -= self.scale
			ring = []
			for j in range(len(previousRing.points)):
				p1Inside = True
				count = 0
				while p1Inside:
					point = self.generate_random_point(previousRing.points[j].parent, previousRing.points[j], 5, count)
					count += 0.05
					p1Inside = previousRing.point_inside(point)
				if (i % 3 == 0):
					p2Inside = True
					count = 0
					while p2Inside:
						middle = simpleGeometry.midpoint(previousRing.points[j], previousRing.points[j-1])
						point2 = self.generate_random_point(self.centrePoint, middle, 5, count)
						count += 0.05
						p2Inside = previousRing.point_inside(point2)
					point2 = self.displace_point(point2)
					if (self.check_point(point2, ring)):
							ring.append(point2)
				point = self.displace_point(point)
				if (self.check_point(point, ring)):
					ring.append(point)
				#arcade.draw_line(previousRing.points[j].x, previousRing.points[j].y, point.x, point.y, arcade.color.WOOD_BROWN, 3)
			contourRing = contour.contourLine(ring, currentElevation)
			self.contours.append(contourRing)
			previousRing = contourRing
			print("Ring " + str(i) + " generated")
		
	def draw(self, surface):
		i = 0
		for ring in reversed(self.contours):
			#print("Ring " + str(i) + " drawing")
			ring.render(surface)
			i += 1
		for d in self.displacements:
			d.draw((255,0,0),1,False,surface)