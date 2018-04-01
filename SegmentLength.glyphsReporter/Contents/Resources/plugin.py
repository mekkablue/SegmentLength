# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

def bezier( P1, P2, P3, P4, t ):
	"""
	Returns coordinates for t (=0.0...1.0) on curve segment.
	x1,y1 and x4,y4: coordinates of on-curve nodes
	x2,y2 and x3,y3: coordinates of BCPs
	"""
	x = P1.x*(1-t)**3 + P2.x*3*t*(1-t)**2 + P3.x*3*t**2*(1-t) + P4.x*t**3
	y = P1.y*(1-t)**3 + P2.y*3*t*(1-t)**2 + P3.y*3*t**2*(1-t) + P4.y*t**3

	return NSPoint(x, y)

def approxLengthOfSegment(segment):
	if len(segment) == 2:
		p0,p1 = segment
		return ( (p1.x-p0.x)**2 + (p1.y-p0.y)**2 )**0.5
	elif len(segment) == 4:
		p0,p1,p2,p3 = segment
		chord = distance(p0,p3)
		cont_net = distance(p0,p1) + distance(p1,p2) + distance(p2,p3)
		return (cont_net + chord) * 0.5 * 0.996767352316
	else:
		print "Segment has unexpected length:\n" + segment

def segmentMiddle(segment):
	if len(segment) == 2:
		p0,p1 = segment
		return NSPoint( (p0.x+p1.x)*0.5, (p0.y+p1.y)*0.5 )
	elif len(segment) == 4:
		p0,p1,p2,p3 = segment
		return bezier(p0,p1,p2,p3,0.5)
	else:
		print "Segment has unexpected length:\n" + segment


class SegmentLength(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Segment Lengths',
			'de': u'Segmentlängen',
		})
		
	def foreground(self, layer):
		for thisPath in layer.paths:
			for thisSegment in thisPath.segments:
				points = [p.pointValue() for p in thisSegment]
				segmentLength = approxLengthOfSegment(points)
				middlePosition = segmentMiddle(points)
				self.drawTextAtPoint( "%.1f"%segmentLength, middlePosition, fontColor=NSColor.redColor() )

	