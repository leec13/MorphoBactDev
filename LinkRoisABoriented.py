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

def initDict(Rois, Zones) :
	dictRois={}
	dictRois.clear()
	for roi in Rois :
		shaperoi = ShapeRoi(roi)
		for zone in Zones :
			zoneshape = ShapeRoi(zone)
			intersect = zoneshape.and(shaperoi)
			if intersect.shapeToRoi().getBounds().width+intersect.shapeToRoi().getBounds().height > 0 :
				dictRois[roi]=(roi,zone)
				continue
	return dictRois

def initSets(Rois, Zones) : 
	
	dictZ={}
	
	for zone in Zones :
		setZoneRois=set()
		setZoneRois.clear()
		
		zoneshape = ShapeRoi(zone)
		for roi in Rois :
			shaperoi = ShapeRoi(roi)
			intersect = shaperoi.and(zoneshape)
			
			if intersect.shapeToRoi().getBounds().width+intersect.shapeToRoi().getBounds().height != 0 : 
				setZoneRois.add(roi)
				#print intersect.shapeToRoi().getBounds().width+intersect.shapeToRoi().getBounds().height
				#print setZoneRois

		if len(setZoneRois) >0 : dictZ[zone]=(zone, setZoneRois)

	return dictZ


def link(RoisA, RoisB, RoisProj) :
	"""
	 This function takes in entry an image, two slices, two arrays of ROIs, a list of coefficients, and a string corresponding to the name of a method.
	 It aims at linking the different ROIs of an image to the ROIs of another image, according to the method and to the coefficients given in entry.
	 It returns 3 lists of tuples :		- one in which the tuples correspond to two ROIs linked.
	 					- another one in which the tuples correspond to new bacteria
	 					- a last one in which the tuples correspond to "lost" bacteria.
	"""	

	# attribuer a chaque RoiA une zone de la projection dans un dictionaire
	
	dictZonesA={}
	dictZonesB={}
	dictRoisA={}
	dictRoisB={}

	rm = RoiManager.getInstance()
	rm.runCommand("reset")
	
	dictRoisA=initDict(RoisA, RoisProj)
	dictRoisB=initDict(RoisB, RoisProj)
	dictZonesA = initSets(RoisA, RoisProj)
	dictZonesB = initSets(RoisB, RoisProj)

	img=IJ.getImage()
	maxArea = img.getWidth()*img.getHeight()
	
	for roia in RoisA : 
		zone = dictRoisA[roia][1]
		shapezone = ShapeRoi(zone)
		roiszone = dictZonesB[zone][1]
		if len(roiszone)==0 :
			print "*****************"
			print "LOST"
		elif len(roiszone)==1 : 
			print "*****************"
			roib = roiszone.pop()
			print "link", roia, " to ", roib
			shapeA = ShapeRoi(roia)
			shapeB = ShapeRoi(roib)
			intersec = shapeB.and(shapeA).shapeToRoi()
			m = Morph(img, intersec)
			if m.Area<maxArea : 
				rm.addRoi(intersec)
				print m.Area
			else : 
				m=Morph(img, roib)
				rm.addRoi(roib)
			
		else :
			print "*****************"
			templist=[]
			for roib in roiszone :
				shapeA = ShapeRoi(roia)
				shapeB = ShapeRoi(roib)
				intersec = shapeB.and(shapeA).shapeToRoi()
				m = Morph(img, intersec)
				if m.Area<maxArea : 
					rm.addRoi(intersec)
					print m.Area
					templist.append(m.Area)
	
	#return (liens,new,lost)
	
if __name__ == "__main__":
	print "start"
	rm = RoiManager.getInstance()
	if (rm==None): rm = RoiManager()
	dir = str(os.path.expanduser(os.path.join("~","Dropbox","MacrosDropBox","py","MorphoBact2", "testmasks","")))
	rm.runCommand("reset")
	#rm.runCommand("Open", "/Users/famille/Dropbox/MacrosDropBox/py/MorphoBact2/testmasks/RoisA.zip")
	rm.runCommand("Open", dir+"RoisA.zip")
	roisa = rm.getRoisAsArray()
	rm.runCommand("reset")
	#rm.runCommand("Open", "/Users/famille/Dropbox/MacrosDropBox/py/MorphoBact2/testmasks/zones.zip")
	rm.runCommand("Open", dir+"zones.zip")
	roisz = rm.getRoisAsArray()
	rm.runCommand("reset")
	#rm.runCommand("Open", "/Users/famille/Dropbox/MacrosDropBox/py/MorphoBact2/testmasks/RoisB.zip")
	rm.runCommand("Open", dir+"RoisB.zip")
	roisb = rm.getRoisAsArray()
	rm.runCommand("reset")
	
	link(roisa, roisb, roisz)
	
	
	
	
	
	
	
	