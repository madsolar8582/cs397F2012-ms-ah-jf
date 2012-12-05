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
#************************** Instructions **************************
# Hiding: Choose the image format, click engage. Then, select the
# image, then the data file. When the program completes, the
# generated file will be in the directory where the program was
# launched from. The file will be called TotallyNotHidden
#
# Retrieval: Choose the image format, click engage. Then, select
# the image. When the program completes, the generated file will be
# in the directory where the program was launched from. The file
# will be called YourData
#******************************************************************

import os, sys, math, struct, time
import Image
import tkFileDialog
import Tkinter
import Tkconstants
import ImageTk
import tkMessageBox

###Error Class###
class Error(Exception):
    #Base error class, used for the rest
    pass

class ExtensionError(Error):
    #Exception raised when someone gives the wrong extension
    #Attributes:
    #   msg -- explanation of the error
    def __init__(self, msg):
        self.msg = msg

class TooMuchDataError(Error):
    #Exception raised when too much data is sent to be hidden
    #Attributes
    #   msg -- explanation of the error
    def __init__(self, msg):
        self.msg = msg
class OutOfBoundsError(Error):
    #Exception raised when you'll wander out of bounds if you keep going
    #Attributes
    #   msg -- explanation of the error
    def __init__(self, msg):
        self.msg = msg

#Function to handle all input/output/errors/derping
def HerpHandler(hideOrNot, imageName, extension, dataPath):
    try:
        if extension[-3:] != imageName[-3:]:
            raise ExtensionError("The image does not match the chosen image type!")
    except ExtensionError as e:
        print "Error Detected:", e.msg
        return 1 #1 for extension error!
    
    if hideOrNot == 0:
        try:
            dataInput = open(dataPath, 'rb') #rb for read!
            Dataz = bytearray(dataInput.read())
        except IOError as e:
            print "Error Detected: IOError, could not open the data file!"
            return 3 #Three for data IO Error
    else:
        Dataz = bytearray()
    try:
        workImage = Image.open(imageName)
    except IOError as e:
        print "Error Detected: IOError, could not open the image file!"
        return 3 #Returns 3 for opening IO error
    #Hand things off to HerpDerper after getting Data/Image
    try:
        HerpDerper(workImage, Dataz, extension)
    except TooMuchDataError as e:
        print "Error Detected:", e.msg
        return 2 #Two for too much data
    except IOError as e:
        print "Error Detected: IOError, can't write data!"
        return 4 #4 for IOError in Derper
    except OutOfBoundsError as e:
        print "Error Detected: Out of Bounds Error!"
        return 5 #5 for out of bounds
    return 0

#HerpDerper does all the derping
#Needs the Image, the Data, and the file extension
#The Image will always be passed as a PIL image object
#Data will be a byte array with length 0 if retrieving, otherwise will contain data to be hidden
#Extension will be the format extension(png, gif, bmp, tiff)
def HerpDerper(workImage, Dataz, extension):
    pixelMap = workImage.load() #Create a pixel map so we can see individual pixels
    pixel = pixelMap[0,0] #The first pixel's value
    (width, height) = workImage.size #Retrieve the images height and width

  ####################Retrieving#########################
    if len(Dataz) == 0:
        timeBegin = time.time() #Start the timer
        if extension == "png":
            print "PNG Retrieval"
            #First retrieve length of data from the first 32 bits
            numPixel = 0
            bitTracker = 0
            msgLen = 33 #Initialize to 33 to retrieve message length, will be reset once found
            lenFound = 0
            retData = ""
            while bitTracker < msgLen:
                if numPixel < (width*height):
                    y = math.floor(numPixel / width)
                    x = numPixel % width
                    pixel = pixelMap[x,y]
                    if pixel[0] % 2 == 1:
                        retData = retData + '1' 
                    else:
                        retData = retData + '0'
                    if pixel[1] % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                    if pixel[2] % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                else:
                    raise OutOfBoundsError("Error Detected: Out of Bounds Error!")
                bitTracker = bitTracker + 3 #Have gone through 3 bits
                if lenFound == 0:
                   numPixel = numPixel + 1
                else:
                   # Work out the formula and apply
                    numPixel = numPixel + keyTwo
                if lenFound == 0 and bitTracker == 33:
                    lenData = retData[:32]
                    retData = retData[32:]
                    msgLen = (int(lenData, 2)) #Msg length in bytes, so mult 8 later to get bits
                    bitTracker = 1 #Set to 1 because still have one bit of the message
                    lenFound = 1
                    #Formula for pixel spacing
                    keyOne = math.ceil(((msgLen+4) * 8) / 3) #See paper p573-roy; +4 accounts for message length int
                    keyTwo = math.floor((width * height) / keyOne) #See above paper, spreads out data based on amount and image size
                    msgLen = msgLen * 8 #Convert to bits

        elif extension == "bmp":
            print "BMP Retrieval"
            #First retrieve length of data from the first 32 bits
            numPixel = 0
            bitTracker = 0
            msgLen = 33 #Initialize to 33 to retrieve message length, will be reset once found
            lenFound = 0
            retData = ""
            while bitTracker < msgLen:
                if numPixel < (width*height):
                    y = math.floor(numPixel / width)
                    x = numPixel % width
                    pixel = pixelMap[x,y]
                    if pixel[0] % 2 == 1:
                        retData = retData + '1' 
                    else:
                        retData = retData + '0'
                    if pixel[1] % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                    if pixel[2] % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                else:
                    raise OutOfBoundsError("Error Detected: Out of Bounds Error!")
                bitTracker = bitTracker + 3 #Have gone through 3 bits
                #Just keep going to the next pixel
                if numPixel % 2 == 0:
                    numPixel = numPixel + 3 
                else:
                    numPixel = numPixel - 1  
                if lenFound == 0 and bitTracker == 33:
                    lenData = retData[:32]
                    retData = retData[32:]
                    msgLen = (int(lenData, 2)) #Msg length in bytes, so mult 8 later to get bits
                    bitTracker = 1 #Set to 1 because still have one bit of the message
                    lenFound = 1
                    msgLen = msgLen * 8 #Convert to bits
        
        elif extension == "tiff":
            print "TIFF Retrieval"
            #First retrieve length of data from the first 32 bits
            numPixel = 0
            bitTracker = 0
            msgLen = 33 #Initialize to 33 to retrieve message length, will be reset once found
            lenFound = 0
            retData = ""
            while bitTracker < msgLen:
                if numPixel < (width*height):
                    y = math.floor(numPixel / width)
                    x = numPixel % width

                    pixel = pixelMap[x,y]
                    if pixel[0] % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                    if pixel[1] % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                    if pixel[2] % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                else:
                    raise OutOfBoundsError("Error Detected: Out of Bounds Error!")
                bitTracker = bitTracker + 3 #Have gone through 3 bits
                #Just keep going to the next pixel
                numPixel = numPixel + 1
                if lenFound == 0 and bitTracker == 33:
                    lenData = retData[:32]
                    retData = retData[32:]
                    msgLen = (int(lenData, 2)) #Msg length in bytes, so mult 8 later to get bits
                    bitTracker = 1 #Set to 1 because still have one bit of the message
                    lenFound = 1
                    msgLen = msgLen * 8 #Convert to bits
    
        elif extension == "gif":
            print "GIF Retrieval"
            #First retrieve length of data from the first 32 bits
            numPixel = 0
            bitTracker = 0
            msgLen = 33 #Initialize to 33 to retrieve message length, will be reset once found
            lenFound = 0
            retData = ""
            while bitTracker < msgLen:
                if numPixel < (width*height):
                    y = math.floor(numPixel / width)
                    x = numPixel % width
                    
                    pixel = pixelMap[x,y]
                    if pixel % 2 == 1:
                        retData = retData + '1'
                    else:
                        retData = retData + '0'
                else:
                    raise OutOfBoundsError("Error Detected: Out of Bounds Error!")
                bitTracker = bitTracker + 1 #Have gone through 1 bit
                #Just keep going to the next pixel
                if numPixel % 2 == 0:
                    numPixel = numPixel + 3 
                else:
                    numPixel = numPixel - 1 
                if lenFound == 0 and bitTracker == 32:
                    lenData = retData[:32]
                    retData = retData[32:]
                    msgLen = (int(lenData, 2)) #Msg length in bytes, so mult 8 later to get bits
                    bitTracker = 0 #Set to 0 because go 1 bit at a time
                    lenFound = 1
                    msgLen = msgLen * 8 #Convert to bits
                        
        else:
            print "Should not have gotten here, please consult the developers immediately..." #No longer possible, since only radio-button choices
            
        #Should now have retData with the full message, might have some extra so slice off anything longer then the message length
        retData = retData[:msgLen]
        bitTracker = 0
        #Output all the data!
        allDataz = bytearray()
        while bitTracker < msgLen:
            tempDataz = int(retData[bitTracker:bitTracker+8], 2)
            Dataz = chr(tempDataz)
            allDataz = allDataz + bytearray(Dataz)
            bitTracker = bitTracker + 8
        dataOutput = open("YourData", 'wb')
        dataOutput.write(allDataz)
        timeEnd = time.time() #End the timer
        print "Retrieval Operation took %0.3f ms" % ((timeEnd-timeBegin)*1000)

  ########################Hiding#########################
    elif len(Dataz) > 0:
        timeBegin = time.time() #Start the timer
        #Need to turn data length into binary data; first thing to be hidden
        binData = bin(len(Dataz))[2:] #Stuff in brackets is to strip off unnecessary 0b at start
        while len(binData) < 32: #Add back in the leading zeroes that were stripped
            binData = '0' + binData
            
        #Now turn the rest of the data into binary data by converting byte array to ints
        #Then the ints to binary strings, and append the binary strings to the master string - look into importing data as binary string
        DataLength = len(Dataz)
        while len(Dataz) % 4 != 0:
            Dataz.append(0x00)  #Ensure no bytes remainder after making ints
        temp = 0
        while temp < len(Dataz):
            tempInt = (Dataz[temp] << 24) + (Dataz[temp+1] << 16) + (Dataz[temp+2] << 8) + Dataz[temp+3] #Create int out of 4 bytes
            tempBin = bin(tempInt)[2:]  #Slice off the 0b
            while len(tempBin) < 32: #Add back in the leading zeroes that were stripped
                tempBin = '0' + tempBin
            binData = binData + tempBin #Join the new binary string to the main one
            temp = temp + 4
        binData = binData + bin(7)[2:] #Add 3 bits to the end to prevent any possible out of bounds exception; will be ignored on retrieval end if used
          
        if extension == "png":
            print "PNG Hiding"
            print "We can fit this much data in KB: %s" % ((((width*height*3)/8) - 4)/1024)
            keyOne = math.ceil(((DataLength+4) * 8) / 3) #See paper p573-roy; +4 accounts for message length int
            keyTwo = math.floor((width * height) / keyOne) #See above paper, spreads out data based on amount and image size
            #Insert data after every keyTwo pixels
            i = 0
            j = 0
            trackBits = 0
            while i < ((DataLength+4) * 8): #8 bits to the byte, can fit 3 bits to the pixel + 1 accounts for message length int
                if j < (width * height): 
                    y = math.floor(j / width)
                    x = j % width
                    pixel = pixelMap[x,y]
                    
                    if binData[trackBits] == '0':
                        tempPixelZero = pixel[0] & 254 #11111110
                    else:
                        tempPixelZero = pixel[0] | 1 #00000001
                    if binData[trackBits + 1] == '0':
                        tempPixelOne = pixel[1] & 254 #11111110
                    else:
                        tempPixelOne = pixel[1] | 1 #00000001
                    #print binData[trackBits + 2]
                    if binData[trackBits+2] == '0':
                        tempPixelTwo = pixel[2] & 254 #11111110
                    else:
                        tempPixelTwo = pixel[2] | 1 #00000001
                    pixelMap[x,y] = (tempPixelZero, tempPixelOne, tempPixelTwo)
                    # First 33 bits will be in the first 11 pixels; will contain message length and first bit of the message
                    #Afterwards, go to pixels keyTwo spaces apart
                    if j < 11:
                        j = j + 1
                    else:
                        j = j + keyTwo #Going to pixels keyTwo spaces apart
                    #Went through 3 bits
                    trackBits = trackBits + 3
                else:
                    raise TooMuchDataError("Error Detected: Too much data to fit!")
                i = i + 3 #Fit 3 bits to the pixel
        
        elif extension == "bmp":
            print "BMP Hiding"
            print "We can fit this much data in KB: %s" % ((((width*height*3-6)/8) - 4)/1024)
            i = 0
            j = 0
            trackBits = 0
            while i < ((DataLength+4) * 8): #8 bits to the byte, can fit 3 bits to the pixel + 1 accounts for message length int
                if j < (width * height): 
                    y = math.floor(j / width)
                    x = j % width
                    pixel = pixelMap[x,y]
                    if binData[trackBits] == '0':
                        tempPixelZero = pixel[0] & 254 #11111110
                    else:
                        tempPixelZero = pixel[0] | 1 #00000001
                    if binData[trackBits + 1] == '0':
                        tempPixelOne = pixel[1] & 254 #11111110
                    else:
                        tempPixelOne = pixel[1] | 1 #00000001
                    if binData[trackBits+2] == '0':
                        tempPixelTwo = pixel[2] & 254 #11111110
                    else:
                        tempPixelTwo = pixel[2] | 1 #00000001
                    pixelMap[x,y] = (tempPixelZero, tempPixelOne, tempPixelTwo)
                    # First 33 bits will be in the first 11 pixels; will contain message length and first bit of the message
                    #Afterwards, continue just moving to the next pixel until out of data
                    if j % 2 == 0:
                            j = j + 3
                    else:
                            j = j - 1
                    #Went through 3 bits
                    trackBits = trackBits + 3
                else:
                    raise TooMuchDataError("Error Detected: Too much data to fit!")
                i = i + 3 #Fit 3 bits to the pixel
                  
        elif extension == "tiff":
            print "TIFF Hiding"
            print "We can fit this much data in KB: %s" % ((((width*height*3)/8) - 4)/1024)
            i = 0
            j = 0
            trackBits = 0
            while i < ((DataLength+4) * 8): #8 bits to the byte, can fit 3 bits to the pixel + 1 accounts for message length int
                if j < (width * height):
                    #Move down, then move to the next column to the right
                    y = math.floor(j / width)
                    x = j % width
                    pixel = pixelMap[x,y]
                    if binData[trackBits] == '0':
                        tempPixelZero = pixel[0] & 254 #11111110
                    else:
                        tempPixelZero = pixel[0] | 1 #00000001
                    if binData[trackBits + 1] == '0':
                        tempPixelOne = pixel[1] & 254 #11111110
                    else:
                        tempPixelOne = pixel[1] | 1 #00000001
                    if binData[trackBits+2] == '0':
                        tempPixelTwo = pixel[2] & 254 #11111110
                    else:
                        tempPixelTwo = pixel[2] | 1 #00000001
                    pixelMap[x,y] = (tempPixelZero, tempPixelOne, tempPixelTwo)
                    # First 33 bits will be in the first 11 pixels; will contain message length and first bit of the message
                    #Afterwards, continue just moving to the next pixel until out of data
                    j = j + 1 #Going to next pixel spaces apart
                    #Went through 3 bits
                    trackBits = trackBits + 3
                else:
                    raise TooMuchDataError("Error Detected: Too much data to fit!")
                i = i + 3 #Fit 3 bits to the pixel

        elif extension == "gif":
            print "GIF Hiding"
            print "We can fit this much data in KB: %s" % (((((width*height - 1)/8) - 4)/1024)) #Use a lot less pixels
            i = 0
            j = 0
            trackBits = 0
            #See Image Palette
            #Fill gifPal with the colors in the palette.  Form RGB
            gifPal = workImage.resize((256,1))
            gifPal.putdata(range(256))
            gifPal = list(gifPal.convert("RGB").getdata())
            while i < ((DataLength+4) * 8): #8 bits to the byte, can fit 3 bits to the pixel + 1 accounts for message length int
                if j < (width * height): 
                    y = math.floor(j / width)
                    x = j % width
                    pixel = pixelMap[x,y]
                    #Gif only has 8 bits to the pixel
                    if binData[trackBits] == '0':
                        tempPixelZero = pixel & 254 #11111110
                        lsb = 0
                    else:
                        tempPixelZero = pixel | 1 #00000001
                        lsb = 1
                    #Now search for an entry in the color palette with the same ending 1 or 0, but closer to the original color
                    orig = gifPal[pixel]
                    Dist = 500
                    while lsb < len(gifPal):
                        newDist = abs(gifPal[lsb][0]- orig[0]) + abs(gifPal[lsb][1] - orig[1]) + abs(gifPal[lsb][2] - orig[2])
                        if newDist < Dist: #and newDist != 0:
                            Dist = newDist
                            tempPixelZero = lsb
                        lsb = lsb + 2
                    
                    pixelMap[x,y] = tempPixelZero
                    # First 32 bits will contain message length
                    #Keep moving forward when j is even, move one backward when odd
                    if j % 2 == 0:
                        j = j + 3  
                    else:
                        j = j - 1  
                    #Went through 1 bit at a time
                    trackBits = trackBits + 1
                else:
                    raise TooMuchDataError("Error Detected: Too much data to fit!")
                i = i+1

        else:
            print "Should not have gotten here, please consult the developers immediately..."
        workImage.save("TotallyNotHidden."+extension, extension)
        timeEnd = time.time() #End the timer
        print "Hiding Operation took %0.3f ms" % ((timeEnd-timeBegin)*1000)
    else:
        #Quit because something is broken in regards to the bytearray
        raise OutOfBoundsError("Error Detected: Out of Bounds Error!")

#GUI Definition, mainly boilerplate code
class App:
    def __init__(self, master):
        
        frame = Tkinter.Frame(master)
        frame.pack()
        hideOrNot = Tkinter.IntVar()
        
        selectionFrame = Tkinter.Frame(frame)
        selectionFrame.pack(side = Tkinter.BOTTOM)
        hidingFrame = Tkinter.Frame(selectionFrame)
        hidingFrame.pack(side = Tkinter.TOP)
        Tkinter.Radiobutton(hidingFrame, text="Hide", variable = hideOrNot, value = 0).pack(side=Tkinter.LEFT)
        Tkinter.Radiobutton(hidingFrame, text="Retrieve", variable = hideOrNot, value = 1).pack(side=Tkinter.RIGHT)
        
        self.titleLabel = Tkinter.Label(frame, text="Hiding Everything in Refactored Pictures")
        self.titleLabel.pack(anchor=Tkinter.CENTER)
        
        im = Image.open("Title.png")
        tkimage = ImageTk.PhotoImage(im)
        self.imageLabel = Tkinter.Label(frame, image=tkimage)
        self.imageLabel.image = tkimage
        self.imageLabel.pack(anchor=Tkinter.CENTER)
        
        extension = Tkinter.StringVar()
        extension.set("png") #Default Initialization
        Tkinter.Radiobutton(selectionFrame, text="PNG", variable = extension, value = "png").pack(side=Tkinter.LEFT)
        Tkinter.Radiobutton(selectionFrame, text="BMP", variable = extension, value = "bmp").pack(side=Tkinter.LEFT)
        Tkinter.Radiobutton(selectionFrame, text="GIF", variable = extension, value = "gif").pack(side=Tkinter.LEFT)
        Tkinter.Radiobutton(selectionFrame, text="TIFF", variable = extension, value = "tiff").pack(side=Tkinter.LEFT)
        
        bottomFrame = Tkinter.Frame(root)
        bottomFrame.pack(side = Tkinter.BOTTOM)
        
        self.quitButton = Tkinter.Button(bottomFrame, text="QUIT", fg="red", command=frame.quit)
        self.quitButton.pack(side=Tkinter.BOTTOM)
        
        self.hi_there = Tkinter.Button(bottomFrame, text="ENGAGE", command=lambda: App.engage(self, hideOrNot, extension))
        self.hi_there.pack(side=Tkinter.BOTTOM)

    def engage(self, hideOrNot, extension):
        hidey = hideOrNot.get()
        ext = extension.get()
        
        if hidey == 0:
            imageFile = tkFileDialog.askopenfilename(title="Hiding: Choose Image File")
            dataFile = tkFileDialog.askopenfilename(title="Hiding: Choose Data File")
            errorCode = HerpHandler(hidey, imageFile, ext, dataFile)
            if errorCode == 1:
                tkMessageBox.showerror("Error",  "The image does not match the chosen image type!")
            elif errorCode == 2:
                tkMessageBox.showerror("Error",  "Too much data to fit")
            elif errorCode == 3:
                tkMessageBox.showerror("Error",  "IOError: Could not open data file or image")
            elif errorCode == 4:
                tkMessageBox.showerror("Error",  "IOError: Could not write to file")
            elif errorCode == 5:
                tkMessageBox.showerror("Error",  "Out of Bounds Error")   
            else:
                tkMessageBox.showinfo("Operation Complete", "Hiding Complete")
        else:
            imageFile = tkFileDialog.askopenfilename(title="Retrieving: Choose Image File")
            errorCode = HerpHandler(hidey, imageFile, ext, None)
            if errorCode == 1:
                tkMessageBox.showerror("Error", "The image does not match the chosen image type!")
            elif errorCode == 2:
                tkMessageBox.showerror("Error", "Too much data to fit")
            elif errorCode == 3:
                tkMessageBox.showerror("Error",  "IOError: Could not open data file or image")
            elif errorCode == 4:
                tkMessageBox.showerror("Error",  "IOError:  Could not write to file")
            elif errorCode == 5:
                tkMessageBox.showerror("Error",  "Out of Bounds Error")  
            else:
                tkMessageBox.showinfo("Operation Complete","Retrieval Complete")
        
if __name__=='__main__':
    root = Tkinter.Tk()
    app = App(root)
    root.mainloop()
