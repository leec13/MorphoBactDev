# -*- coding: iso-8859-15 -*-

import javax.swing as swing
import java.awt as awt
from javax.swing import BorderFactory
from javax.swing.border import EtchedBorder, TitledBorder
from java.awt import TextField, Panel, GridLayout, ComponentOrientation, Label, Checkbox, BorderLayout, Button, Color, FileDialog, Frame, Font


from ij import ImageStack, ImagePlus, WindowManager, IJ
from ij.gui import Roi, NonBlockingGenericDialog, Overlay
from ij.plugin.frame import RoiManager
from ij.plugin.filter import MaximumFinder

import sys
import os
import time
import glob
import os.path as path
import getpass
import shutil
import random
import math

username=getpass.getuser()

#mypath=os.path.expanduser(IJ.getDirectory("plugins")+"MeasureCells")
mypath=os.path.expanduser(os.path.join("~","Dropbox","MacrosDropBox","py","MorphoBact2"))
sys.path.append(mypath)

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from MorphoBact import Morph
from RangeRois import RangeRois

class OptionsDialog(swing.JFrame):
	def __init__(self): 
		swing.JFrame.__init__(self, title="Option Dialog")
		self.setDefaultCloseOperation(swing.JFrame.DISPOSE_ON_CLOSE)

		self.__zonedir = IJ.getDirectory("image")
		self.__zonesfile = ""
		self.oked = False
		self.run()
	
	def run(self) :
		self.size=(450, 200)
		self.contentPane.layout = awt.BorderLayout()
		line = BorderFactory.createEtchedBorder(EtchedBorder.LOWERED)

		#-------- NORTH --------------
		
		northpanel=swing.JPanel(awt.FlowLayout(awt.FlowLayout.LEFT))
		northpanel.setBorder(line)
		#zonesfile = swing.JButton("Select zones file... ", size=(100, 70), actionPerformed=self.__zones)
		#northpanel.add(zonesfile)

		panel0=Panel()
		zonesfile = swing.JButton("Select zones file... ", size=(100, 70), actionPerformed=self.__zones)
		self.__filezonespath = TextField(self.__zonedir+self.__zonesfile)
		panel0.add(zonesfile)
		panel0.add(self.__filezonespath)
		northpanel.add(panel0)
		

		#-------- CENTER --------------
		grid = awt.GridLayout()
		grid.setRows(2)

		centerpanel=swing.JPanel(grid)
		centerpanel.setBorder(line)

		labelparam1=swing.JLabel("Param1")
		labelparam1.setText("Param1 ?")
		centerpanel.add(labelparam1)
		self.__valparam1 = swing.JTextField(preferredSize=(30, 30), horizontalAlignment=swing.SwingConstants.LEFT)
		self.__valparam1.text = "11"
		centerpanel.add(self.__valparam1)
		self.__boxparam1=swing.JCheckBox(actionPerformed=self.__actboxparam1)
		self.__boxparam1.setText("Boolean param1")
		self.__boxparam1.setSelected(False)
		centerpanel.add(self.__boxparam1)


		labelparam2=swing.JLabel("Param2")
		labelparam2.setText("Param2 ?")
		centerpanel.add(labelparam2)
		self.__valparam2 = swing.JTextField(preferredSize=(30, 30), horizontalAlignment=swing.SwingConstants.LEFT)
		self.__valparam2.text = "11"
		centerpanel.add(self.__valparam2)
		self.__boxparam2=swing.JCheckBox(actionPerformed=self.__actboxparam2)
		self.__boxparam2.setText("Boolean param2")
		self.__boxparam2.setSelected(False)
		centerpanel.add(self.__boxparam2)

		

		#-------- SOUTH --------------
		southpanel=swing.JPanel(awt.FlowLayout(awt.FlowLayout.RIGHT))
		southpanel.setBorder(line)
		
		help = swing.JButton("Help", size=(100, 70), actionPerformed=self.__help)
		close = swing.JButton("Close", size=(100, 70), actionPerformed=self.__close)

		southpanel.add(help)
		southpanel.add(close)		
		
		self.contentPane.add(northpanel, awt.BorderLayout.NORTH)
		#self.contentPane.add(westpanel, awt.BorderLayout.WEST)
		self.contentPane.add(centerpanel, awt.BorderLayout.CENTER)
		#self.contentPane.add(eastpanel, awt.BorderLayout.EAST)
		self.contentPane.add(southpanel, awt.BorderLayout.SOUTH)

	def __zones(self, event):
		self.__zonedir=IJ.getDirectory("image")
		#self.__pathdir=IJ.getDirectory("")
		frame = Frame("Zones file ROIS ?")
		fd = FileDialog(frame)
		fd.setDirectory(self.__zonedir)
		fd.show()
		self.__zonedir = fd.getDirectory() 
		self.__zonesfile = fd.getFile()
		self.__filezonespath.text=(self.__zonedir+self.__zonesfile)
		print self.__zonedir+self.__zonesfile
	
	def __close(self, event):
		self.oked = True
		time.sleep(0.01) 
		self.dispose()
		
	def __help(self, event):
		IJ.log("help")

	def __actboxparam1(self, event):
		self.__bparam1 = event.getSource().isSelected()

	def __actboxparam2(self, event):
		self.__bparam2 = event.getSource().isSelected()

# ------ end ---------------

if __name__ == "__main__":

	op=OptionsDialog()
	op.show()