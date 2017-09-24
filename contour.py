import simpleGeometry
import elevationColours
import pygame

class contourPoint(simpleGeometry.simplePoint):

	def __init__(self, x, y, parent):
		super(contourPoint, self).__init__(x, y)
		self.parent = parent
		self.parentDistance = simpleGeometry.distance_between(parent, self)
		
	@staticmethod
	def create_from_simplePoint(point, parent):
		return contourPoint(point.x, point.y, parent)
		
		
class contourLine(simpleGeometry.simplePolygon):

	def __init__(self, pointList, elevation):
		super(contourLine, self).__init__(pointList)
		self.elevation = elevation
		
	def render(self, surface):
		self.draw(elevationColours.fill[self.elevation], 1, True, surface)
		self.draw(elevationColours.line[self.elevation], 2, False, surface)
		
	@staticmethod
	def create_from_simplePolygon(polygon, elevation):
		return contourLine(polygon.points, elevation)