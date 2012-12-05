#!/usr/bin/env python
#******************************************************************
# Authors: Andrew Heien, Madison Solarana, & Jon Fauser
# Class: CS 397 - Fall 2012
# Instructor: Dr. Kessentini
# Program: H.E.R.P. (Hiding Everything in Retouched Pictures)
# License: Academic Free License ("AFL") v. 3.0
# License Link: <http://opensource.org/licenses/AFL-3.0>
#************************** Requirements **************************
# This program requires Python 2.7.x to run, NOT Python 3.3.x!
# This program requires the Python Imaging Library (PIL) to run
# This program requires PyUnit for the associated unit tests
# This program requires Tkinter for GUI components
#************************** Compatibility *************************
# Tested on Mac OS X 10.7.5 (11G63) & Python 2.7.1
# Tested on Mac OS X 10.8.2 (12C60) & Python 2.7.3
#******************************************************************
import unittest
import HERPProgram
import Image

class Testing(unittest.TestCase):
    
    def setUp(self):
        self.pngImage = Image.open("TestPNG.png")
        self.assertEqual((478, 640), self.pngImage.size) #Sizes from image properties
        self.gifImage = Image.open("TestGIF.gif")
        self.assertEqual((650, 475), self.gifImage.size)
        self.tiffImage = Image.open("TestTIFF.tiff")
        self.assertEqual((600,600), self.tiffImage.size)
        self.bmpImage = Image.open("TestBMP.bmp")
        self.assertEqual((800,600), self.bmpImage.size)
        dataInput = open("testTextData.txt", 'rb')
        self.data = bytearray(dataInput.read())
        self.assertEqual(71, len(self.data))
        dataInput.close()
        
    def testHandler(self):
        #These errors are all caught in HerpHandler, so check to see it returns the correct value for the exception
        self.assertEqual(3, HERPProgram.HerpHandler(0, "Nonexistent.png", "png", "Nonexistent.data")) #3 for IOError
        self.assertEqual(3, HERPProgram.HerpHandler(1, "Nonexistent.png", "png", None)) #returns 3 for IOError
        self.assertEqual(1, HERPProgram.HerpHandler(0, "TestBMP.bmp", "png", "testData.txt"))   #Returns 1 for ExtensionError
        self.assertEqual(1, HERPProgram.HerpHandler(0, "TestBMP.png", "gif", "testData.txt"))   #Returns 1 for ExtensionError
        self.assertEqual(1, HERPProgram.HerpHandler(0, "TestBMP.gif", "tiff", "testData.txt"))   #Returns 1 for ExtensionError
        self.assertEqual(1, HERPProgram.HerpHandler(0, "TestBMP.tiff", "bmp", "testData.txt"))   #Returns 1 for ExtensionError
        
    def testDerper(self):
        #Open link to original data file
        #Hide Data in a png
        self.assertEqual(71, len(self.data)), "Before First Hiding"
        HERPProgram.HerpDerper(self.pngImage, self.data, "png")
        #Now retrieve it
        newImage = Image.open("TotallyNotHidden.png")
        self.assertEqual(newImage.size, self.pngImage.size)
        HERPProgram.HerpDerper(newImage, bytearray(), "png")
        #Reset self.data
        dataInput = open("testTextData.txt", 'rb')
        self.data = bytearray(dataInput.read())
        dataInput.close()
        pngDataInput = open("YourData", 'rb')
        newData = bytearray(pngDataInput.read())
        self.assertEqual(len(newData), len(self.data)), "PNG: Retrieved data not same length"

        #Same for gif
        #Hide Data in a gif
        HERPProgram.HerpDerper(self.gifImage, self.data, "gif")
        #Now retrieve it
        newImage = Image.open("TotallyNotHidden.gif")
        self.assertEqual(newImage.size, self.gifImage.size)
        HERPProgram.HerpDerper(newImage, bytearray(), "gif")
        #Reset self.data
        dataInput = open("testTextData.txt", 'rb')
        self.data = bytearray(dataInput.read())
        dataInput.close()
        gifDataInput = open("YourData", 'rb')
        newData = bytearray(gifDataInput.read())
        self.assertEqual(len(newData), len(self.data)), "GIF: Retrieved data not same length"
        
        #Same for tiff
        #Hide Data in a tiff
        HERPProgram.HerpDerper(self.tiffImage, self.data, "tiff")
        #Now retrieve it
        newImage = Image.open("TotallyNotHidden.tiff")
        self.assertEqual(newImage.size, self.tiffImage.size)
        HERPProgram.HerpDerper(newImage, bytearray(), "tiff")
        #Reset self.data
        dataInput = open("testTextData.txt", 'rb')
        self.data = bytearray(dataInput.read())
        dataInput.close()
        tiffDataInput = open("YourData", 'rb')
        newData = bytearray(tiffDataInput.read())
        self.assertEqual(len(newData), len(self.data)),"TIFF: Retrieved data not same length"
                 
        #Same for bmp
        #Hide Data in a bmp
        HERPProgram.HerpDerper(self.bmpImage, self.data, "bmp")
        #Now retrieve it
        newImage = Image.open("TotallyNotHidden.bmp")
        self.assertEqual(newImage.size, self.bmpImage.size)
        HERPProgram.HerpDerper(newImage, bytearray(), "bmp")
        #Reset self.data
        dataInput = open("testTextData.txt", 'rb')
        self.data = bytearray(dataInput.read())
        dataInput.close()
        bmpDataInput = open("YourData", 'rb')
        newData = bytearray(bmpDataInput.read())
        self.assertEqual(len(newData), len(self.data)), "BMP: Retrieved data not same length"
        
        #Test raising of TooMuchDataError
        largeInput = open("TestBMP.bmp", 'rb')
        largeByteArray = bytearray(largeInput.read())
        #HerpDerper does not catch Exceptions, so check to see if exception raised for too much data
        self.assertRaises(HERPProgram.TooMuchDataError, HERPProgram.HerpDerper, self.bmpImage, largeByteArray, "bmp")
                          
if __name__=='__main__':
    unittest.main()
