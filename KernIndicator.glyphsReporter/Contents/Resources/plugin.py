# encoding: utf-8
from __future__ import division, print_function, unicode_literals

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
from Foundation import NSPointInRect, NSPoint, NSRect

class KernIndicator(ReporterPlugin):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Kerning Values',
			'de': u'Kerning-Werte',
			'es': u'valores de Kerning',
			'fr': u'les valeurs de crénage',
		})
		
		# offset value
		Glyphs.registerDefault( "com.mekkablue.KernIndicator.offset", 150 )
		if Glyphs.defaults["com.mekkablue.KernIndicator.offset"] is None:
			Glyphs.defaults["com.mekkablue.KernIndicator.offset"] = 150
	
	@objc.python_method
	def foreground(self, layer):
		scale = self.getScale()
		if not 0.0299 < scale < 0.9001:
			return
			
		positiveColor = NSColor.systemOrangeColor()
		negativeColor = NSColor.systemBlueColor()
		offset = 600
		try:
			offset += int(Glyphs.defaults["com.mekkablue.KernIndicator.offset"])
		except:
			pass
		
		# go through tab content
		glyph = layer.glyph()
		font = layer.font()
		if font: # sometimes font is empty, don't know why
			tab = font.currentTab
			tabView = tab.graphicView()
			layerCount = tabView.cachedLayerCount()
			if layerCount>1:
				viewPort = tab.viewPort
				viewPort.origin.y -= layer.ascender()*scale
				activePosition = tabView.activePosition()
				previousLayer = tabView.cachedGlyphAtIndex_(0)
				for i in range(1,layerCount):
					thisLayer = tabView.cachedGlyphAtIndex_(i)
					thisLayerPosition = tabView.cachedPositionAtIndex_(i)
					if NSPointInRect( thisLayerPosition, viewPort ) and type(thisLayer) != GSControlLayer and type(previousLayer) != GSControlLayer:
						previousMasterID = previousLayer.master.id
						thisMasterID = thisLayer.master.id
						if thisMasterID == previousMasterID:
							leftGlyph = previousLayer.glyph()
							rightGlyph = thisLayer.glyph()
							if leftGlyph and rightGlyph:
								kerningValue = font.kerningForFontMasterID_firstGlyph_secondGlyph_( thisMasterID, leftGlyph, rightGlyph )
								if kerningValue and kerningValue < 10000: #notfound
									offsetVector = subtractPoints(thisLayerPosition, activePosition)
									textPoint = NSPoint( offsetVector.x/self.getScale() - 0.5*kerningValue, offsetVector.y/self.getScale() + offset )
									if kerningValue < 0:
										self.drawTextAtPoint( str(int(kerningValue)), textPoint, fontColor=negativeColor, align="bottomcenter" )
									else:
										self.drawTextAtPoint( str(int(kerningValue)), textPoint, fontColor=positiveColor, align="bottomcenter" )
								
					previousLayer = thisLayer

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
