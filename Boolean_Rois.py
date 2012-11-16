# -*- coding: iso-8859-15 -*-

import sys
import os
import glob
import os.path 
import getpass
import math

from ij import IJ
from ij.gui import Roi, ShapeRoi


from java.lang import Double,Boolean

#mypath=os.path.expanduser(IJ.getDirectory("plugins")+"MeasureCells")
mypath=os.path.expanduser(os.path.join("~","Dropbox","MacrosDropBox","py","MorphoBact2"))
sys.path.append(mypath)

username=getpass.getuser()

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from MorphoBact import Morph

def inter(roia, roib) :
	shapeA = ShapeRoi(roia)
	shapeB = ShapeRoi(roib)
	intersect = shapeB.and(shapeA).shapeToRoi()
	if intersect.isArea() and intersect.getType()>0 :
		mask=intersect.getMask()
		pixels = mask.getIntArray()
		area = sum([sum(v) for v in pixels])/255
		
	else : area = 0
	
	return [intersect, area]

def union(roia, roib) :
	pass


if __name__ == "__main__":
	print "start"

	rm = RoiManager.getInstance()
	rois = rm.getRoisAsArray()
	a = inter(rois[0], rois[1])
	print a


	
