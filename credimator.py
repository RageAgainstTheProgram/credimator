# This file is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

# This program creates video credits from a simple textfile. 
# Simply write your content in the program-secific syntax and it 
# will generate your credits.

# Copyright (c) 2023  Lars Wichmann 

# Version 2.0.0

import cv2
import os
import tempfile
import re
import argparse
from matplotlib import font_manager
from termcolor import colored
from pathlib import Path
from PIL import Image , ImageDraw, ImageFont
from sys import exit


class Block():
    def __init__(self, headline, level, blockType, column, data, blockstyle, blockSpacing, headlineTopSpaecing, headlineTextSpace, lineSpace, blockOffset, textSize):

        printMessage(message="--------Creating block-------", messageType = 'debug')

        if headline == None:
            printMessage(message="Block data: " + blockType + ", " + str(len(data)) + " block elements", messageType="debug")
        else:
            printMessage(message="Block data: " + headline + ", " + level  + ", " + blockType + ", " + str(len(data)) + " block elements", messageType="debug")


        self.headline = headline
        self.level = level
        self.type = blockType
        self.style = blockStyle
        self.data = data
        self.textSize = textSize
        #handle blockSpacing
        if blockSpacing != None:
            self.headlineTopSpacing = blockSpacing[0]
            self.headlineTextSpace = blockSpacing[1]
            self.textSize = blockSpacing[2]
            self.lineSpace = blockSpacing[3]
            self.blockOffset = blockSpacing[4]
        else:
            self.headlineTopSpacing = None
            self.headlineTextSpace = None
            self.textSize = textSize
            self.lineSpace = None
            self.blockOffset = None

        #print(str(self.headlineTopSpacing) + ", " + str(self.headlineTextSpace) + ", " + str(self.textSize) + ", " + str(self.lineSpace) + ", " + str(self.blockOffset))

        if column != None:
            self.column = int(column)
        else:
            self.column = None

        if self.textSize is None:
            #self.textSize = textSize
            self.textSize = int(videoWidth / 100)
            printMessage(message = 'Set textsize to: ' + str(self.textSize), messageType = 'debug')

        self.headlineSize = self.getHeadlineSize(level)

        if self.lineSpace != None:
            self.lineSpace = self.lineSpace
        elif lineSpaceSettings != None and lineSpace != None:
            self.lineSpace = lineSpace
            printMessage(message = 'Set linespace from block: ' + str(self.lineSpace), messageType = 'debug')
        elif lineSpaceSettings != None and lineSpace == None:
            self.lineSpace = lineSpaceSettings
            printMessage(message = 'Set linespace from setting: ' + str(self.lineSpace), messageType = 'debug')
        else:
            self.lineSpace = int(0.3 * self.textSize)
            printMessage(message = 'Set default linespace: ' + str(self.lineSpace), messageType = 'debug')

        if self.blockOffset != None:
            self.blockOffset = self.blockOffset
        elif blockOffsetSettings != None and blockOffset != None:
            self.blockOffset = blockOffset
            printMessage(message = 'Set blockOffset from block: ' + str(self.blockOffset), messageType = 'debug')
        elif blockOffsetSettings != None and blockOffset == None:
            self.blockOffset = blockOffsetSettings
            printMessage(message = 'Set blockOffset from setting: ' + str(self.blockOffset), messageType = 'debug')
        else:
            self.blockOffset = int(2 * textSize)
            printMessage(message = 'Set default blockOffset: ' + str(self.blockOffset), messageType = 'debug')
       
       
        if headline != None:

            printMessage(message = 'Creating layout spacing for headline: ' + "'" + str(self.headline) + "'", messageType = 'debug')
            

        if self.headlineTopSpacing != None:
            self.headlineTopSpacing = self.headlineTopSpacing
        elif headlineTopSpacing == None:
            #calculate dafault depending on level
            self.headlineTopSpacing = self.getHeadlineTopSpacing(level)
            printMessage(message = 'Calculating default headline top spacing: ' + str(self.headlineTopSpacing), messageType = 'debug')
        else:
            self.headlineTopSpacing = headlineTopSpacing
            printMessage(message = 'Set headline top spacing from block: ' + str(self.headlineTopSpacing), messageType = 'debug')


        if self.headlineTextSpace != None:
            self.headlineTopSpacing = self.headlineTopSpacing
        elif headlineTextSpace == None:
            self.headlineTextSpace = self.getHeadlineTextSpace(level)
            printMessage(message = 'Calculating headline text spacing: ' + str(self.headlineTextSpace), messageType = 'debug')
        else:
            self.headlineTextSpace = headlineTextSpace
            printMessage(message = 'Set headline top spacing from block: ' + str(self.headlineTextSpace), messageType = 'debug')
            
   
    def getHeadlineSize(self, level):
        
        match level:
            case "h0":
                return int(2.5 * self.textSize)
            case "h1":
                return int(2.2 * self.textSize)
            case "h2":
                return int(1.8 * self.textSize)
            case "h3":
                return int(1.5 * self.textSize)
            case "h4":
                return int(1.3 * self.textSize)
            case "h5":
                return int(1.2 * self.textSize)
            case "h6":
                return self.textSize
        
    def getHeadlineTopSpacing(self, level):
        
        match level:
            case "h0":
                return int(1 * self.blockOffset)
            case "h1":
                return int(0.85 * self.blockOffset)
            case "h2":
                return int(0.6 * self.blockOffset)
            case "h3":
                return int(0.4 * self.blockOffset)
            case "h4" | "h5" | "h6":
                return int(0.3 * self.blockOffset)
        
    def getHeadlineTextSpace(self, level):
        
        match level:
            case "h0":
                return int(2.5 * self.headlineSize)
            case "h1":
                return int(2.25 *  self.headlineSize)
            case "h2":
                return int(1.75 *  self.headlineSize)
            case "h3":
                return int(1.75 *  self.headlineSize)
            case "h4" | "h5" | "h6":
                return int(1.5 *  self.headlineSize)
            
    def printSpacing(self):

        if self.headline is not None:
            printMessage(message= "-----" + self.headline + "-----", messageType= "message", forcePrint = True)
            printMessage(message= "level: " + self.level, messageType= "message", forcePrint = True)
        else:
            printMessage(message= "-----" + self.level + "-----", messageType= "message", forcePrint = True)

        printMessage(message= "headline size: " + str(self.headlineSize), messageType= "message", forcePrint = True)
        printMessage(message= "headline top spacing: " + str(self.headlineTopSpacing), messageType= "message", forcePrint = True)
        printMessage(message= "headline text spacing: " + str(self.headlineTextSpace), messageType= "message", forcePrint = True)
        printMessage(message= "text size: " + str(self.textSize), messageType= "message", forcePrint = True)
        printMessage(message= "line space: " + str(self.lineSpace), messageType= "message", forcePrint = True)
        printMessage(message= "block offset: " + str(self.blockOffset), messageType= "message", forcePrint = True)
    
        

class FontAction(argparse.Action):

    SUPPRESS = '==SUPPRESS=='

    def __init__(self,
                 option_strings,
                 version=None,
                 dest=SUPPRESS,
                 default=SUPPRESS,
                 help="show program's version number and exit"):
        super(FontAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)
        
    def __call__(self, parser, namespace, values, option_string=None):
        fonts = sorted(font_manager.findSystemFonts())
        
        maxPathLength = 0
        maxNameLength = 0

        for fontPath in fonts:
            if "Emoji" not in fontPath and "18030" not in fontPath:
                font = ImageFont.FreeTypeFont(fontPath)
                name, weight = font.getname()

                if len(fontPath) > maxPathLength:
                    maxPathLength = len(fontPath)
                if len(name) > maxNameLength:
                    maxNameLength = len(name)

        for filename in fonts:
            if "Emoji" not in filename and "18030" not in filename:
                font = ImageFont.FreeTypeFont(filename)
                name, weight = font.getname()
                filename = filename.ljust(maxPathLength, " ")
                name = name.ljust(maxNameLength, " ")

                printMessage(message= filename + " name: " + name + " weight: " + weight, messageType="message", forcePrint=True)

        parser.exit()
        

def printMessage(messageType, pos = None, progPos = None, message = '', forceExit = False, forcePrint = False, inline = False):

    if force:
        forceExit = False

    if outputMessage or debug or forcePrint:
        if messageType == 'status':
            print(colored(message, 'green'))
        if messageType == 'info':
            print(colored(message, 'cyan'))
        if messageType == 'message':
            if inline:
                print(message, flush= True, end = "")
            else:
                print(message)
        
        if debug:
            if messageType == "debug":
                print(colored(message, "yellow"))

    if messageType == 'syntaxError':
        if message == '':
            print(colored("Syntax error in line: " + str(pos), 'red'))
        else:
            print(colored(message, 'red'))
            print(colored("Syntax error in line: " + str(pos), 'red'))
        if debug:
            print(colored(str(progPos), 'yellow'))
    
    if messageType == 'error':
        print(colored(message, 'red'))
        
    if forceExit:
        exit(-1)



def getAndSetPixel(textInput, mode):

    textStartY = 0
    posCounter = 0
    firstRun = True
    global columnWidth
    global imgDraw

    
    for block in textInput:

        localTextSize = block.textSize
        localLineSpace = block.lineSpace
        localBlockOffset = block.blockOffset

        imgFontRegular = ImageFont.truetype(imgFontRegularSettings, localTextSize)
        imgFontBold = ImageFont.truetype(imgFontBoldSettings, localTextSize)

        match block.type:
            case 'tuple':
                match block.style:
                    case "rb":
                        mainImgFont = imgFontBold
                        additionalImgFont = imgFontRegular
                        printMessage(message="Use default tuple style from settings", messageType='debug')
                    case "br":
                        mainImgFont = imgFontRegular
                        additionalImgFont = imgFontBold
                        printMessage(message="Use default tuple style from settings", messageType='debug')
                    case "rr":
                        mainImgFont = imgFontRegular
                        additionalImgFont = imgFontRegular
                        printMessage(message="Use default tuple style from settings", messageType='debug')
                    case "bb":
                        mainImgFont = imgFontBold
                        additionalImgFont = imgFontBold
                        printMessage(message="Use default tuple style from settings", messageType='debug')
                    case None:
                        mainImgFont = imgFontBold
                        additionalImgFont = imgFontRegular
                        printMessage(message="Use default tuple style from default", messageType='debug')
            case 'box':
                match block.style:
                    case "b":
                        mainImgFont = imgFontBold
                        printMessage(message="Use default box style from settings", messageType='debug')
                    case "r":
                        mainImgFont = imgFontRegular
                        printMessage(message="Use default box style from settings", messageType='debug')
                    case None:
                        mainImgFont = imgFontBold
                        printMessage(message="Use default box style from default", messageType='debug')
            case 'table':
                match block.style:
                    case "b":
                        mainImgFont = imgFontBold
                        printMessage(message="Use default table style from settings", messageType='debug')
                    case "r":
                        mainImgFont = imgFontRegular
                        printMessage(message="Use default table style from settings", messageType='debug')
                    case None:
                        mainImgFont = imgFontBold
                        printMessage(message="Use default table style from default", messageType='debug')
            case 'text':
                match block.style:
                    case "b":
                        mainImgFont = imgFontBold
                        printMessage(message="Use default table style from settings", messageType='debug')
                    case "r":
                        mainImgFont = imgFontRegular
                        printMessage(message="Use default table style from settings", messageType='debug')
                    case None:
                        mainImgFont = imgFontBold
                        printMessage(message="Use default table style from default", messageType='debug')



        #check for headlines and create if available
        if block.headline != None:
            headline = block.headline
            headlineSize = block.headlineSize
            headlineFont = ImageFont.truetype(imgFontBoldSettings, headlineSize)
            headlineTopSpacing = block.headlineTopSpacing
            headlineTextSpace = block.headlineTextSpace

            if tmpImgDraw.textlength(headline, headlineFont) <= maxTextWidth:
                if firstRun:
                    firstRun = False
                    textStartY += headlineSize
                    if mode == 'set':
                        imgDraw.text((imageCenter, textStartY), headline, textColor, headlineFont, anchor= "md", align = 'center')
                else:
                    textStartY += headlineSize + headlineTopSpacing
                    if mode == 'set':
                        imgDraw.text((imageCenter, textStartY), headline, textColor, headlineFont, anchor= "md", align = 'center')
                if block.data != []:
                    textStartY += headlineTextSpace
                    printMessage(message="Adding headline text space: " + str(headlineTextSpace) + " for headline: " + headline, messageType="debug")

            else:
                printMessage(message = "headline does not fit into textbox: " + "'" + headline + "'", messageType = 'error', forceExit = True)
        
        if block.style != None:

            printMessage(message="Set style of blocktype " + block.type + " to: " + block.style, messageType='debug')

            if block.type == 'tuple':
                match block.style:
                    case "rb":
                        mainImgFont = imgFontBold
                        additionalImgFont = imgFontRegular
                    case "br":
                        mainImgFont = imgFontRegular
                        additionalImgFont = imgFontBold
                    case "rr":
                        mainImgFont = imgFontRegular
                        additionalImgFont = imgFontRegular
                    case "bb":
                        mainImgFont = imgFontBold
                        additionalImgFont = imgFontBold
            elif block.type == 'box':
                match block.style:
                    case "b":
                        mainImgFont = imgFontBold
                    case "r":
                        mainImgFont = imgFontRegular
            elif block.type == 'table':
                match block.style:
                    case "b":
                        mainImgFont = imgFontBold
                    case "r":
                        mainImgFont = imgFontRegular
            elif block.type == 'text':
                match block.style:
                    case "b":
                        mainImgFont = imgFontBold
                    case "r":
                        mainImgFont = imgFontRegular
        else:
            printMessage(message="Set style from settings", messageType='debug')
        
    
        if block.data == []:
            continue

        #create layout for blocktype tuple
        if block.type == "tuple":
            for content in block.data:

                if content[0] == '§':
                    textStartY += localTextSize + localLineSpace
                    continue

                textStartY += localTextSize + localLineSpace
                maxLine = int ((maxTextWidth / 2) - tupleSpace)

                if tmpImgDraw.textlength(content[0], font = additionalImgFont) > maxLine:

                    lineSplit = content[0].split()
                    printMessage(message="Line split: " + str(lineSplit), messageType="debug")
                    
                    string = ""
                    
                    for word in lineSplit:

                        printMessage(message="Word to add: " + word, messageType='debug')
                        if string == "":
                            if tmpImgDraw.textlength(word, font = additionalImgFont) <= maxLine:
                                string += word
                                printMessage(message="First element: " + string, messageType="debug")
                            else:
                                if mode == 'set':
                                    imgDraw.text((imageCenter - int(tupleSpace / 2), textStartY), string, textColor, font=additionalImgFont, anchor = 'rd')
                                string = word
                                printMessage(message="Start new line with: " + string, messageType='debug')
                                textStartY += localTextSize + localLineSpace
                        else:
                            if tmpImgDraw.textlength(string + " " + word, font = additionalImgFont) <= maxLine:
                                string += " " + word
                                printMessage(message="Add element: " + word + " to string: " + string, messageType="debug")
                            else:
                                if mode == 'set':
                                    imgDraw.text((imageCenter - int(tupleSpace / 2), textStartY), string, textColor, font=additionalImgFont, anchor = 'rd')
                                string = word
                                printMessage(message="Start new line with: " + string, messageType='debug')
                                textStartY += localTextSize + localLineSpace
 
                    if mode == 'set':
                        imgDraw.text((imageCenter - int(tupleSpace / 2), textStartY), string, textColor, font=additionalImgFont, anchor = 'rd')
                        imgDraw.text((imageCenter + int(tupleSpace / 2), textStartY), content[1], textColor, font=mainImgFont, anchor = 'ld')
                else:
                    if mode == 'set':
                        imgDraw.text((imageCenter - int(tupleSpace / 2), textStartY), content[0], textColor, font=additionalImgFont, anchor = 'rd')
                        imgDraw.text((imageCenter + int(tupleSpace / 2), textStartY), content[1], textColor, font=mainImgFont, anchor = 'ld')
            textStartY += localBlockOffset

        #create layout for blocktype box
        elif block.type == "box":
            string = ""
            for content in block.data:
                if tmpImgDraw.textlength(string + ' ' + boxSeparator + ' ' + content[0], font = mainImgFont) <= maxTextWidth:
                    if string == "":
                        string += content[0]
                        continue
                    string += ' ' + boxSeparator + ' ' + content[0]
                    continue
                else:
                    textStartY += localTextSize + localLineSpace
                    if mode == 'set':
                        imgDraw.text((imageCenter, textStartY), string, textColor, font=mainImgFont, anchor= "md", align = 'center')
                    string = content[0]
            textStartY += localTextSize + localLineSpace
            if mode == 'set':
                imgDraw.text((imageCenter, textStartY), string, textColor, font=mainImgFont, anchor= "md", align = 'center')
            textStartY += localBlockOffset
        
        #create layout for blocktype table
        elif block.type == "table":
            
            #calculate number of columns if not set
            if block.column == None:
                if len(block.data) >= 24:
                    column = 3
                else:
                    column = 2
            else:
                column = block.column

            #get largest content and set column width
            for content in block.data:
                currentLength = tmpImgDraw.textlength(content[0], font = mainImgFont)
                if currentLength > columnWidth:
                    columnWidth = currentLength

            leftSpace = int((videoWidth - ((column - 1) *  columnSpace + column * columnWidth)) / 2)

            if leftSpace < int(border / 2):
                printMessage(message = "can not fit text into textbox: " + content[0], forceExit = True, messageType = 'error')

            posColumn = leftSpace + int(columnWidth / 2)
            posCounter = 0

            for content in block.data:
                mod = posCounter % column
                posCounter += 1
                if mode == 'set':
                    imgDraw.text((posColumn + mod * (columnWidth + columnSpace), textStartY), content[0], textColor, font=mainImgFont, anchor= "mm", align = 'center')

                if mod == column -1 or content[0] == block.data[-1][0]:
                    textStartY += localTextSize + localLineSpace
            textStartY += localBlockOffset
        
        elif block.type == "text":

            string = ""
            
            for content in block.data:

                if content[0] == '§':
                        textStartY += localTextSize + localLineSpace
                        if mode == 'set':
                            imgDraw.text((imageCenter, textStartY), string, textColor, font=mainImgFont, anchor= "md", align = 'center')
                        textStartY += localTextSize + localLineSpace
                        string = ""
                        continue
                
                for word in content[0].split():
                    if tmpImgDraw.textlength(string + " " + word, font= mainImgFont) < maxTextWidth:
                        if string == "":
                            string += word
                        else:
                            string += " " + word
                        continue
                    else:
                        textStartY += localTextSize + localLineSpace
                        if mode == 'set':
                            imgDraw.text((imageCenter, textStartY), string, textColor, font=mainImgFont, anchor= "md", align = 'center')
                        string = word
            textStartY += localTextSize + localLineSpace
            if mode == 'set':
                imgDraw.text((imageCenter, textStartY), string, textColor, font=mainImgFont, anchor= "md", align = 'center')
            textStartY += localBlockOffset




    #add offset to bottom of image to get all fit all content
    if len(textInput[-1].data) < 0:
        textStartY -= localBlockOffset + localLineSpace
    else:
        textStartY -= localBlockOffset - localLineSpace

    if enableSignature:
        signatureSize = int(localTextSize/1.75)
        signatureFont = ImageFont.truetype(imgFontBoldSettings, signatureSize)
        textStartY += 6 * localBlockOffset + signatureSize
        #check why i have to use 2 * signatureSize

        if mode == 'set':
            watermark = "Credits layouted by credimator. Visit credimator on github.com to learn more."
            imgDraw.text((imageCenter, textStartY), watermark, textColor, font=signatureFont, anchor= "md", align = 'center')

        textStartY += localLineSpace



    if mode == 'get':
        printMessage(message = "Done calculating overlay image height", messageType = 'status')
        return textStartY
    
    if mode == 'set':
        textImg.save(overlayImageName + 'overlayText.png', format = 'PNG')
        printMessage(message = "Done creating overlay image", messageType = 'status')



#debug settings
debug =  None
outputMessage = None
force = None
printSpacing = None


#video settings
videoWidth = 1920
videoHeight = 1080
fps = 25
backgroundColor = (0, 0, 0, 1)
speed = 5
possibleCvVideoFormat = ['.mov', '.avi', '.mp4']
videoformat = ""
outFileName = ""
inputFile = None
videoOut = None

#overlay image and text settings
overlayImagePath = tempfile.TemporaryDirectory()
overlayImageName = os.path.join(overlayImagePath.name, "tmpVideoOut.mov")
imageFileFormat = ".bmp"
textSize = None
lineSpace = None
textColor = (255, 255, 255)

tupleStyle = None
boxStyle = None
tableStyle = None
textStyle = None

columnSpace = 100
border = 200
tupleSpace = 20
columnWidth = 0
imageHeight = 0
headlineTextSpace = None
boxSeparator = '•'
blockOffset = None
headlineTopSpacing = None
headlineTextSpace = None
imgFontRegularSettings = None
imgFontBoldSettings = None
blockSpacing = None

#block settings
headline = ""
level = ""
blockType = ""
column = 0
currentBlockContent = []
textInput = []
blockOffsetSettings = None
lineSpaceSettings = None

enableSignature = True


#parse command-line input
parser = argparse.ArgumentParser(description='This is a program to create credits from a textfile', prefix_chars='-')

parser.add_argument('-d', action='store_true', dest='debug', default= False, help='enable debug mode')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='enable verbose')
parser.add_argument('-f', '--force', action='store_true', dest='force', default=False, help='enable force mode')
parser.add_argument('input', help="input textfile to generate credits", action = 'store')
parser.add_argument('output', help="path to the generated video including filename", nargs= "?", default= "None" ,action = 'store')
parser.add_argument('--fonts', action = FontAction, dest='fonts', default=False, help='print all available font types')
parser.add_argument('--spacing', action = 'store_true', dest='spacing', default=False, help='print spacing for current file')
parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')

parserResult = parser.parse_args()

if parserResult.fonts:
    printMessage(message= font_manager.get_font_names(), messageType='message', forcePrint=True, forceExit=True)


debug = parserResult.debug
outputMessage = parserResult.verbose
force = parserResult.force
printSpacing = parserResult.spacing
inputFile = parserResult.input

if parserResult.output == "None":
    videoOutPath = os.path.splitext(parserResult.input)[0]
    print(videoOutPath)
    videoformat = ".mov"
    videoOutPath += videoformat
    videoOut = videoOutPath
else:
    videoOutPath = Path(parserResult.output)
    videoformat = videoOutPath.suffix
    videoOut = parserResult.output

printMessage(message= "Done creating video filename: " + videoOut, messageType='debug')




with open(inputFile, encoding = 'utf-8') as file:

    printMessage(message="Reading file from: " + inputFile, messageType='debug')

    fileContent = file.read()
    lines = fileContent.split("\n")

    state = "readSettings"
    lineCounter = 0
    
    for line in lines:
        lineCounter += 1
        hashInLine = False
        posHash = line.find("#")

        if posHash >= 0:
            line = line[:line.find("#")]
            hashInLine = True

        if re.match("^\s*$", line):
            if hashInLine:
                continue
            if state == 'readSettings' or state == 'findHeader':
                continue
            continue

        match = re.search("^(\w+)\s*(\w*)\s*=\s*(\(?([^ \t]+\s*,?\s*)*\)?)\s*$", line)
        if match:
            if state == "readSettings":
                key1 = match.group(1).strip()
                key2 = match.group(2).strip()
                value = match.group(3).strip()

                if key2 == "":
                    printMessage(message = "Reading " + key1 + " from settings: " + value, messageType ='debug')
                else:
                    printMessage(message = "Reading " + key1 + " " + key2 + " from settings: " + value, messageType ='debug')

                if key1 == "width":
                    videoWidth = int(value)
                    continue
                if key1 == "height":
                    videoHeight = int(value)
                    continue
                if key1 == "fps":
                    fps = int(value)
                    continue
                if (key1 == "background" and key2 == "color" or key2 == "colour"):
                    backgroundColor = eval(value)
                    continue
                if (key1 == "text" and key2 == "color" or key2 == "colour"):
                    textColor = eval(value)
                    continue
                if key2 == 'style':
                    if key1 == 'tuple' and value in ['rb', 'br', 'bb' , 'rr']:
                        tupleStyle = value
                        continue
                    if key1 == 'box' and value in ['r', 'b']:
                         boxStyle = value
                         continue
                    if key1 == 'table' and value in ['r', 'b']:
                        tableStyle = value
                        continue
                    if key1 == 'text' and value in ['r', 'b']:
                        textStyle = value
                        continue
                    if key1 == 'tuple' and value not in ['rb', 'br', 'bb' , 'rr']:
                        printMessage(message = 'Could not store style: ' + tupleStyle + '. Please choose from: rb, br, bb , rr',pos = lineCounter, progPos =0, messageType = 'syntaxError', forceExit = True)
                        continue
                    if key1 == 'table' or 'box' or 'text' and value not in ['r', 'b']:
                        printMessage(message = 'Could not store style: ' + tupleStyle + '. Please choose from: r, b',pos = lineCounter, progPos =0, messageType = 'syntaxError', forceExit = True)
                if key1 == "text" and key2 == "size":
                    textSize = int(value)
                    continue
                if key1 == "line" and key2 == "space":
                    lineSpaceSettings = int(value)
                    continue
                if key1 == "speed":
                    speed = int(value)
                    continue
                if key1 == 'border':
                    border = 2 * int(value)
                    continue
                if key1 == 'box' and key2 == 'separator':
                    boxSeparator = value
                    continue
                if key1 == 'tuple' and key2 == 'space':
                    tupleSpace = int(value)
                    continue
                if key1 == 'block' and key2 == 'offset':
                    blockOffsetSettings = int(value)
                    continue
                if key1 == 'regular' and key2 == 'font':
                    imgFontRegularSettings = value
                    continue
                if key1 == 'bold' and key2 == 'font':
                    imgFontBoldSettings = value
                    continue
                if key1 == 'enable' and key2 == 'signature':
                    if value in ['true', 'True']:
                        enableSignature = True
                    elif value in ['false', 'False']:
                        enableSignature = False
                    
                    continue
                printMessage(message = 'Unknwon setting. Please check spelling',pos = lineCounter, progPos =0, messageType = 'syntaxError', forceExit = True)

                continue
            else:
                printMessage(pos = lineCounter, progPos =1, messageType = 'syntaxError', forceExit = True)

                

        #match = re.search("^(\*([^\*]+)\*)?\(((h[0-6])\s*,?)?\s*(table|box|tuple|text)?(\s*,\s*([2-3])\s*)?\s*\)\s*\{\s*$", line)
        #match = re.search("^(\*([^\*]+)\*)?\(((h[0-6])\s*,?)?\s*(table|box|tuple|text)?(\s*,\s*([2-3])\s*)?\s*(,\s*([rb]{1,2}))?\s*\)\s*\{\s*$", line)
        match = re.search("^(\*([^\*]+)\*)?\(((h[0-6])\s*,?)?\s*(table|box|tuple|text)?(\s*,\s*([2-3])\s*)?\s*(,\s*([rb]{1,2}))?\s*(,\s*\((((\s*[\d-]*\s*)?\s*,?\s*){5})\s*\)\s*)?\)\s*\{\s*$", line)
        if match:
            if state == "findHeader" or state == "readSettings":
                state = "readHeader"

                if match.group(5) == None:
                    headline = match.group(2)
                    level = match.group(4)
                    continue
                headline = match.group(2)
                level = match.group(4)
                blockType = match.group(5)
                column = match.group(7)
                blockStyle = match.group(9)

                if match.group(11) != None:

                    inputSpace = match.group(11).replace("-1", "None")

                    printMessage(message = "Read space: " + inputSpace, messageType = 'debug')

                    blockSpacing = eval(inputSpace)

                if blockStyle != None:

                    if blockType == 'tuple' and match.group(9) in ['br', 'bb', 'rb', 'rr']:
                        blockStyle = match.group(9)
                    elif blockType in ['box', 'table', 'text'] and match.group(9) in ['r', 'b']:
                        blockStyle = match.group(9)
                    else:
                        printMessage(message = "Wrong style for blocktype: " + blockType + ". Could not set style: " + blockStyle, pos = lineCounter, progPos =3, messageType = 'syntaxError', forceExit = True)


                continue
                printMessage(pos = lineCounter, progPos =2, messageType = 'syntaxError', forceExit = True)

            else:
                printMessage(message = "Worng block definition in state: " + state, pos = lineCounter, progPos =3, messageType = 'syntaxError', forceExit = True)

        match = re.search("^\s*(([^:}]+):)?\s*([^\n}]+)$", line)
        if match:
            if state == "readBlock" or state == "readHeader":
                state = "readBlock"

                value1 = match.group(2)
                value2 = match.group(3)

                if value1 == None:
                    currentBlockContent.append((value2,))
                else:
                    value1 = value1.strip()
                    currentBlockContent.append((value1, value2))
                continue
            else:
                printMessage(pos = lineCounter, progPos =4, messageType = 'syntaxError', forceExit = True)
        
        if re.match("^\s*}\s*$", line):
            if state == "readBlock" or state == "readHeader":
                state = "findHeader"

                #save data
                textInput.append(Block(headline, level, blockType, column, currentBlockContent, blockStyle, blockSpacing, headlineTopSpacing, headlineTextSpace, lineSpace, blockOffset, textSize))
                
                printMessage(message = "Clear variables for next block", messageType ='debug')
                headline = None
                level = None
                blockType = None
                column = None
                currentBlockContent = []
                blockOffset = None
                headlineTextSpace = None
                headlineTopSpacing = None
                lineSpace = None
                blockStyle = None
                blockSpacing = None
                blockType = None
                #print("textSize: " + str(textSize))
                continue
            else:
                printMessage(pos = lineCounter, progPos =5, messageType = 'syntaxError', forceExit = True)

        printMessage(pos = lineCounter, progPos =6, messageType = 'syntaxError', forceExit = True)

imageCenter = int(videoWidth / 2)
maxTextWidth = videoWidth - border



printMessage(message = "Done parsing and creating data", messageType = "status")

#create overlay image with transperent background
tmpImg = Image.new(mode =  "RGBA", size = (videoWidth, imageHeight), color = (255, 255, 255, 0))
tmpImgDraw = ImageDraw.Draw(tmpImg)
     
#get image height
imageHeight = getAndSetPixel(textInput, 'get')

textImg = Image.new(mode =  "RGBA", size = (videoWidth, imageHeight), color = (255, 255, 255, 0))
imgDraw = ImageDraw.Draw(textImg)


#pillow

#set text to image
getAndSetPixel(textInput, 'set')

if printSpacing:

    for level in ["h0", "h1", "h2", "h3", "h4", "h5", "h6"]:
        block = Block(None, level, "", None, [], None, None, None, None, None, None, None)
        block.printSpacing()

    for block in textInput:
        block.printSpacing()
    exit()


if os.path.exists(videoOut):
    if debug or force or input("File allready exists. Do you want to overwrite existing file (y/n)? ") == 'y':
        os.remove(videoOut)
        printMessage(message= "Delete existing version of: " + videoOut, messageType = 'info')
    else:
        printMessage(message="Please change filename", messageType= 'message', forceExit=True, forcePrint=True)


#create video

if videoformat in possibleCvVideoFormat:
    outFileName = videoOut
else:
    tmpVideoPath = tempfile.TemporaryDirectory()
    outFileName = os.path.join(tmpVideoPath.name, "tmpVideoOut.mov")
out = cv2.VideoWriter(outFileName, cv2.VideoWriter_fourcc(*'MJPG'), fps, (videoWidth, videoHeight))
printMessage(message="Creating video using: " + outFileName, messageType="debug")



#create progress bar
progressBar = 30

mod = int(((imageHeight + videoHeight)/speed) / progressBar)
printMessage(message='[', messageType='message', inline= True)
for x in range(0, int((imageHeight + videoHeight)/speed)):
    if x % mod == mod - 1:
        printMessage(message='#', messageType='message', inline= True)
printMessage(message='] \n[', messageType='message', inline= True)

#paste text image on background and send to video
with tempfile.NamedTemporaryFile(suffix = imageFileFormat) as tmpDirect:
    for x in range(0, int((imageHeight + videoHeight)/speed)):
        

        if x % mod == mod - 1:
            printMessage(message='#', messageType='message', inline= True)


        tmpPath = tmpDirect.name

        backgroundImg = Image.new(mode = "RGBA", size = (videoWidth, videoHeight), color = backgroundColor)

        #paste image. nackgroundImg.paste(textImg, (0, videoHeight - speed * x), textImg) also works
        backgroundImg.alpha_composite(textImg, (0, videoHeight - speed * x))
        backgroundImg.save(tmpPath, format = 'BMP')

        #add image to video
        imgToVideo = cv2.imread(tmpPath)
        out.write(imgToVideo)
    
    printMessage(message=']', messageType='message')
#save video
out.release()



if videoformat not in possibleCvVideoFormat:
    command = "ffmpeg -i " + outFileName + " " + videoOut
    os.system(command)
    printMessage(message= "Delete tmp file: " + outFileName, messageType='debug')
    os.remove(outFileName)
    printMessage(message= "Delete tmp path: " + tmpVideoPath.name, messageType='debug')
    os.rmdir(tmpVideoPath.name)

printMessage(message = 'Done creating video. checkout video in: ' + videoOut, messageType = 'status')