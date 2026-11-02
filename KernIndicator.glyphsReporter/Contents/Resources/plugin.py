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
from GlyphsApp import Glyphs, GSControlLayer, subtractPoints
from GlyphsApp.plugins import ReporterPlugin
from Foundation import NSPoint
from AppKit import NSColor

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
		Glyphs.registerDefault( "com.mekkablue.KernIndicator.offset", -50 )
		if Glyphs.defaults["com.mekkablue.KernIndicator.offset"] is None:
			del Glyphs.defaults["com.mekkablue.KernIndicator.offset"]
	
	@objc.python_method
	def foreground(self, layer):
		scale = self.getScale()
		if not 0.0299 < scale < 0.9001:
			return
			
		positiveColor = NSColor.systemOrangeColor()
		negativeColor = NSColor.systemBlueColor()
		if hasattr(Glyphs, 'versionNumber') and Glyphs.versionNumber >= 3 :
			# GLYPHS 3
			offset = layer.master.defaultAscender()
		else:
			# GLYPHS 2
			offset = layer.master.ascender
		
		try:
			offset += int(Glyphs.defaults["com.mekkablue.KernIndicator.offset"])
		except:
			pass
		
		# go through tab content
		font = layer.font()
		if font: # sometimes font is empty, don't know why
			tab = font.currentTab
			tabView = tab.graphicView()
			layerCount = tabView.cachedLayerCount()
			if layerCount>1:
				activePosition = tabView.activePosition()
				if Glyphs.versionNumber >= 4:
					# Glyphs 4 renamed cachedGlyphAtIndex_ and added the writing direction to the kerning lookup
					direction = tab.writingDirection()
					previousLayer = tabView.cachedLayerAtIndex_(0)
				else:
					previousLayer = tabView.cachedGlyphAtIndex_(0)
				for i in range(1,layerCount):
					if Glyphs.versionNumber >= 4:
						thisLayer = tabView.cachedLayerAtIndex_(i)
					else:
						thisLayer = tabView.cachedGlyphAtIndex_(i)
					thisLayerPosition = tabView.cachedPositionAtIndex_(i)
					# no culling against tab.viewPort: in Glyphs 4 it left values only in a zone
					# near the bottom center of the window (see forum report)
					if not isinstance(thisLayer, GSControlLayer) and not isinstance(previousLayer, GSControlLayer):
						previousMasterID = previousLayer.master.id
						thisMasterID = thisLayer.master.id
						if thisMasterID == previousMasterID:
							leftGlyph = previousLayer.glyph()
							rightGlyph = thisLayer.glyph()
							if leftGlyph and rightGlyph:
								if Glyphs.versionNumber >= 4:
									kerningValue = font.kerningForFontMasterID_firstGlyph_secondGlyph_direction_( thisMasterID, leftGlyph, rightGlyph, direction )
								else:
									kerningValue = font.kerningForFontMasterID_firstGlyph_secondGlyph_( thisMasterID, leftGlyph, rightGlyph )
								if kerningValue and kerningValue < 10000: #notfound
									offsetVector = subtractPoints(thisLayerPosition, activePosition)
									textPoint = NSPoint( offsetVector.x/scale - 0.5*kerningValue, offsetVector.y/scale + offset )
									if kerningValue < 0:
										self.drawTextAtPoint( str(int(kerningValue)), textPoint, fontColor=negativeColor, align="bottomcenter" )
									else:
										self.drawTextAtPoint( str(int(kerningValue)), textPoint, fontColor=positiveColor, align="bottomcenter" )
					previousLayer = thisLayer

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
