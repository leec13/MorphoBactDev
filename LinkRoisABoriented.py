# -*- coding: iso-8859-15 -*-

import sys
import os
import glob
import os.path 
import getpass
import math

from ij import IJ
from ij.gui import Roi, ShapeRoi
from ij.plugin.frame import RoiManager
from ij import ImageStack, ImagePlus, WindowManager
from ij.gui import Roi, NonBlockingGenericDialog, Overlay
from ij.process import ImageProcessor


from java.lang import Double,Boolean

#mypath=os.path.expanduser(IJ.getDirectory("plugins")+"MeasureCells")
mypath=os.path.expanduser(os.path.join("~","Dropbox","MacrosDropBox","py","MorphoBact2"))
sys.path.append(mypath)

username=getpass.getuser()

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from MorphoBact import Morph
import Boolean_Rois

imp = IJ.getImage()
delta=100.00
attribute = "Area"

def initDict(Rois, Zones) :
	dictRois={}
	dictRois.clear()
	for roi in Rois :
		for zone in Zones :
			intersect = Boolean_Rois.inter(roi, zone)
			if intersect[1] > 0 :
				dictRois[roi]=(roi,zone)
				continue
	return dictRois

def initSets(Rois, Zones) : 
	
	dictZ={}
	
	for zone in Zones :
		setZoneRois=set()
		setZoneRois.clear()
		for roi in Rois :
			intersect = Boolean_Rois.inter(roi, zone)
			if intersect[1] > 0 : setZoneRois.add(roi)
		dictZ[zone]=(zone, setZoneRois)
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


	#for r in RoisA : print "A", r.getName()
	#for r in RoisB : print "B", r.getName()
	
	dictZonesA={}
	dictZonesB={}
	dictRoisA={}
	dictRoisB={}

	liens=[]
	new=[]
	lost=[]
	findlost=[]

	rm = RoiManager.getInstance()
	rm.runCommand("reset")
	
	dictRoisA=initDict(RoisA, RoisProj)
	dictRoisB=initDict(RoisB, RoisProj)
	dictZonesA = initSets(RoisA, RoisProj)
	dictZonesB = initSets(RoisB, RoisProj)

	img=IJ.getImage()
	maxArea = img.getWidth()*img.getHeight()
	
	for roia in RoisA :
		if roia in dictRoisA.keys() :
			zone = dictRoisA[roia][1]
			roiszone = dictZonesB[zone][1]
			if len(roiszone)==0 :
				#print "*****************"
				#print roia.getName(),"LOST"
				lost.append(("LOST",roia))
			elif len(roiszone)==1 : 
				#print "*****************"
				roib = roiszone.pop()
				#print "link", roia.getName(), " to ", roib.getName()
				liens.append((roia,roib))
				#rm.addRoi(roib)
				#findlost.append(RoisB.index(roib))
				continue
			else :
				intersectlist=[]
				noninterlist=[]
				tempdict={}
				for roib in roiszone :
					intersect = Boolean_Rois.inter(roia, roib)
					if intersect[1] > 0 :
						intersectlist.append(roib)
						tempdict[intersect[1]]=roib
					
					else : 
						noninterlist.append(roib)
			
				if len(intersectlist)>1 : 
					key=max(tempdict.keys())
					#rm.addRoi(tempdict[key])
					#print "*****************"
					#print "link", roia.getName(), " to ", tempdict[key].getName()
					liens.append((roia,tempdict[key]))
					#findlost.append(RoisB.index(tempdict[key]))
					roiszone.remove(tempdict[key])
					continue
				
				elif len(intersectlist)==1 :
					#rm.addRoi(intersectlist[0])
					#print "*****************"
					#print "link", roia.getName(), " to ", intersectlist[0].getName()
					liens.append((roia,intersectlist[0]))
					#findlost.append(RoisB.index(intersectlist[0]))
					roiszone.remove(intersectlist[0])
					continue
			
				else :
					if len(noninterlist)>1 :
						ma = Morph(imp, roia)
						maxdist=10000
						print "-----"
						for cible in noninterlist :
							mb = Morph(imp, cible)
							val = [(1,ma.XC,mb.XC), (1,ma.YC,mb.YC)]
							d = Morph.distMorph(val)
							print d
							if d < maxdist : 
								candidate = cible
								maxdist = d
							
						liens.append((roia,candidate))
						print "plusieurs cibles, link ", roia.getName(), "-", candidate.getName()
						roiszone.remove(candidate)
						continue
					elif len(noninterlist) == 1 :
						#rm.addRoi(noninterlist[0])
						#print "*****************"
						#print "link", roia.getName(), " to ", noninterlist[0].getName()
						liens.append((roia,noninterlist[0]))
						roiszone.remove(noninterlist[0])
						#findlost.append(RoisB.index(noninterlist[0]))
					
					else :
						print "jamais ici", roia.getName()


	for roisB in RoisB	:
		marqueurtemp = False
		for lien in liens :
			if lien[1] == roisB :
				marqueurtemp = True
				break
		if marqueurtemp == False :
			new.append(("NEW",roisB))

	return (liens, new, lost)
	
	# selection des cellules comprises dans le criteres acceptables

def sortLiens(liens, losts) :
	for l in liens :
		roia, roib =l[0], l[1]
		ma, mb = Morph(imp, roia), Morph(imp, roib)
		measurea = ma.__getattribute__(attribute)
		measureb = mb.__getattribute__(attribute)
		if (measurea-measureb)/measurea < delta*(-1) and delta > 0 :
			losts.append(("LOST", l[0]))
			liens.remove(l)
		elif (measurea-measureb)/measurea > delta*(-1) and delta < 0 :
			losts.append(("LOST", l[0]))
			liens.remove(l)
		else : continue	

	return (liens, losts)
			
	
if __name__ == "__main__":
	
	rm = RoiManager.getInstance()
	if (rm==None): rm = RoiManager()
	dir = str(os.path.expanduser(os.path.join("~","Dropbox","MacrosDropBox","py","MorphoBact2", "testmasks","")))
	rm.runCommand("reset")
	#rm.runCommand("Open", "/Users/famille/Dropbox/MacrosDropBox/py/MorphoBact2/testmasks/RoisA.zip")
	rm.runCommand("Open", dir+"RoiSetT01.zip")
	roisa = rm.getRoisAsArray()
	rm.runCommand("reset")
	#rm.runCommand("Open", "/Users/famille/Dropbox/MacrosDropBox/py/MorphoBact2/testmasks/zones.zip")
	rm.runCommand("Open", dir+"zones.zip")
	roisz = rm.getRoisAsArray()
	rm.runCommand("reset")
	#rm.runCommand("Open", "/Users/famille/Dropbox/MacrosDropBox/py/MorphoBact2/testmasks/RoisB.zip")
	rm.runCommand("Open", dir+"RoiSetT40.zip")
	roisb = rm.getRoisAsArray()
	rm.runCommand("reset")
	
	links = link(roisa, roisb, roisz)
	liens = links[0]
	new = links[1]
	lost = links[2]

	rm.runCommand("reset")
	#for l in liens :
	#	rm.addRoi(l[0])
	#	rm.addRoi(l[1])

	rm.runCommand("reset")
	for l in new :
		rm.addRoi(l[1])

	rm.runCommand("reset")
	for l in lost :
		rm.addRoi(l[1])
	

	

	
	
	
	
	
	
	
	