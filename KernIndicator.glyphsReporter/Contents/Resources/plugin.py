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

class KernIndicator(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Kerning Values',
			'de': u'Kerning-Werte',
			'es': u'valores de Kerning',
			'fr': u'valeurs de crénage',
		})
		
	def foreground(self, layer):
		positiveColor = NSColor.systemOrangeColor()
		negativeColor = NSColor.systemBlueColor()
		
		# go through tab content
		glyph = layer.glyph()
		font = layer.font()
		if font: # sometimes font is empty, don't know why
			tabView = font.currentTab.graphicView()
			layerCount = tabView.cachedLayerCount()
			lineOfLayers = []
			lineOfOffsets = []
			maxHeight = 600.0 # where to draw the kerning value
			
			# collect layers in the same line (to only draw the marks we need)
			for i in range(layerCount):
				thisLayer = tabView.cachedGlyphAtIndex_(i)
			
				# collect layers and their offsets except newlines
				if type(thisLayer) != GSControlLayer:
					lineOfLayers.append( thisLayer )
					lineOfOffsets.append( tabView.cachedPositionAtIndex_(i) )
					layerBounds = thisLayer.bounds
					maxHeight = max( maxHeight, layerBounds.origin.y+layerBounds.size.height+150 )
			
				# if we reach end of line or end of text, draw with collected layers:
				if type(thisLayer) == GSControlLayer or i==layerCount-1:
					previousLayer = None
					# step through all layers of the line:
					for j, thisLayerInLine in enumerate(lineOfLayers):
						if previousLayer and previousLayer.associatedFontMaster().id == thisLayerInLine.associatedFontMaster().id:
							masterID = thisLayerInLine.associatedFontMaster().id
							leftGlyph = previousLayer.glyph()
							rightGlyph = thisLayerInLine.glyph()
		
							kerningValue = None
							if leftGlyph and rightGlyph:
								kerningValue = font.kerningForFontMasterID_firstGlyph_secondGlyph_( masterID, leftGlyph, rightGlyph )
								if kerningValue > 10000: #notfound
									kerningValue = None
							
							if not kerningValue is None:
								activePosition = tabView.activePosition()
								lastLayerInLinePosition = tabView.cachedPositionAtIndex_(i)
								thisLayerInLinePosition = lineOfOffsets[j]
								offset = subtractPoints(thisLayerInLinePosition, activePosition)
								textPoint = NSPoint( offset.x/self.getScale() - 0.5*kerningValue, offset.y/self.getScale() + maxHeight )
								if kerningValue < 0:
									self.drawTextAtPoint( str(int(kerningValue)), textPoint, fontColor=negativeColor, align="bottomcenter" )
								else:
									self.drawTextAtPoint( str(int(kerningValue)), textPoint, fontColor=positiveColor, align="bottomcenter" )
									
						previousLayer = thisLayerInLine
				
					# reset layer collection and maxHeight
					lineOfLayers = []
					lineOfOffsets = []
					maxHeight = 600.0
		

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
