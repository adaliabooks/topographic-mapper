import arcade
import pygame
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
		
	def __eq__(self, point):
		return self.convert_to_tuple() == point.convert_to_tuple()
	
	def __ne__(self, point):
		return not self == point
		
	def convert_to_tuple(self):
		return (self.x, self.y)
		
	def draw(self, colour, size, surface):
		#arcade.draw_point(self.x, self.y, colour, size)
		pygame.draw.line(surface, colour, [self.x, self.y], [self.x, self.y], size)
		
class simpleEdge():

	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		self.length = distance_between(p1, p2)
		
	def draw(self, colour, size, surface):
		#arcade.draw_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, colour, size)
		pygame.draw.line(surface, colour, [self.p1.x, self.p1.y], [self.p2.x, self.p2.y], size)
		
class simpleCircle():

	def __init__(self, centre, radius):
		self.centre = centre
		self.radius = radius
		
	def point_inside(self, point):
		dist = distance_between(self.centre, point)
		if (dist <= self.radius):
			return True
		else:
			return False
		
	def draw(self, colour, size, filled, surface):
		if (filled):
			#arcade.draw_circle_filled(self.centre.x, self.centre.y, self.radius, colour)
			pygame.draw.circle(surface, colour, [self.centre.x, self.centre.y], self.radius)
		else:
			#arcade.draw_circle_outline(self.centre.x, self.centre.y, self.radius, colour, size)
			pygame.draw.circle(surface, colour, [self.centre.x, self.centre.y], self.radius, size)
			
class simpleEllipse():

	def __init__(self, centre, xRadius, yRadius, angle):
		self.centre = centre
		self.xRadius = xRadius
		self.yRadius = yRadius
		self.angle = angle
		
	def point_inside(self, point):
		cosa=math.cos(self.angle)
		sina=math.sin(self.angle)
		dx=self.xRadius/2*self.xRadius/2
		dy=self.yRadius/2*self.yRadius/2

		a =math.pow(cosa*(point.x-self.centre.x)+sina*(point.y-self.centre.y),2)
		b =math.pow(sina*(point.x-self.centre.x)-cosa*(point.y-self.centre.y),2)
		ellipse=(a/dx)+(b/dy)

		if ellipse <= 1:
			return True
		else:
			return False
			
	def draw(self, colour, size, filled, surface):
		if (filled):
			#arcade.draw_ellipse_filled(self.centre.x, self.centre.y, self.xRadius, self.yRadius, colour, self.angle)
			aRect = pygame.Rect([self.centre.x - self.xRadius, self.centre.y - self.yRadius, self.xRadius*2, self.yRadius*2])
			aRect.normalize()
			pygame.draw.ellipse(surface, colour, aRect)
		else:
			#arcade.draw_ellipse_outline(self.centre.x, self.centre.y, self.xRadius, self.yRadius, colour, size, self.angle)
			aRect = pygame.Rect([self.centre.x - self.xRadius, self.centre.y - self.yRadius, self.xRadius*2, self.yRadius*2])
			aRect.normalize()
			pygame.draw.ellipse(surface, colour, aRect, size)
	
class simplePolygon():

	def __init__(self, pointList):
		self.points = pointList
		self.edges = []
		for i in range(len(self.points)):
			edge = (self.points[i],self.points[i-1])
			self.edges.append(edge)
			
	def point_inside(self, point):

		poly = deepcopy(self.points)
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
		
	def draw(self, colour, size, filled, surface):
		pointList = []
		for point in self.points:
			pointList.append(point.convert_to_tuple())
		if (filled):
			pygame.draw.polygon(surface, colour, pointList, 0)
		else:
			pygame.draw.polygon(surface, colour, pointList, size)
		
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
	
def generate_polygon(centre, minDist, maxDist, numberOfPoints, randomise=True):
	random.seed()
	angleRange = 360/numberOfPoints
	points = []
	for index in range(numberOfPoints):
		dist = random.uniform(minDist, maxDist)
		if (randomise):
			angle = math.radians(random.uniform(index * angleRange, (index + 1) * angleRange))
		else:
			angle = math.radians(angleRange)
		x = dist * math.sin(angle) + centre.x
		y = dist * math.cos(angle) + centre.y
		points.append(simplePoint(x, y))
	poly = simplePolygon(points)
	return poly