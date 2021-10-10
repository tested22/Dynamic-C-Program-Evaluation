"""TODO:
attempt to match printfs and scanfs

match printfs to labdescriptor output names
if single printf and or scanf, check the order
otherwise when matched between input and  printf has been made, 
check if scanf closest to it fits possible data type, if so match scanf closest to it

attempt to match inputs to scanfs/printfs - if matching does not complete skip lab make match probabilistic
generate script
parse script for answer
handle files
fopen redirect their command to open my test file instead
debugging by checking every lab
CONVERT LINE NUMBER TO ORDER
    -Have LIST OF FUNCTIONS searched for while reading lines of code to generate scan list
        -CREATE LIST OF FUNCTIONS
DETERMINE IF THE SCANF IS REPETITIVE
    -Check for scanf in list of loops
        -list of loops for, while, do-while
    -Determine how the loop terminates
CONVERT FORMAT STRING TO EACH INDIVIDUAL ELEMENT
    -separate string based on '%' character as delimiter

handle when u need to compile with specific libraries
check for these libaries
math.h
thread.h?

if they are off by a small amount, check for it and only subtract a little

if no matches, could try brute forcing every test with that many # of inputs... 
may need human judgement 

any printf that is after the last scanf can be discarded because it is simply output and definitely not a prompt
"""
import os, sys, threading, thread, re, math, string
from string import *
from time import sleep
rosterPath = "./roster.txt"
assignmentsPath = "./"
descriptorPath = "./loan.txt"

#rosterPath = "C:/Users/Neil/Desktop/1057R/roster.txt"
#assignmentsPath = "C:/Users/Neil/Desktop/1057R/loan/"
#descriptorPath = "C:/Users/Neil/Desktop/1057R/4/loan.txt"
#def deletePrintStatements():

class input:
    def __init__(self, names,dataTypes,testValue):
        self.__names = names
        self.__dataTypes = dataTypes
        self.__testValue = testValue
    def getNames(self):
	return self.__names
    def getDataTypes(self):
	return self.__dataTypes
    def getTestValue(self):
	return self.__testValue
    def printMe(self):
        print "Input: Possible Names- ", self.__names, " Possible Data Types- ", self.__dataTypes, "Program Test Value- ", self.__testValue

class output:
    def __init__(self, searchStrings):
        self.__searchStrings = searchStrings
    def getsearchStrings(self):
	return self.__searchStrings
    def printMe(self):
        print "Output: Accepted Answers- ", self.__searchStrings

""" class roundingError:
    def __init__(self, lowerBound, upperBound):
	self.__lowerBound = lowerBound
	self.__upperBound = upperBound	        
    def getLowerBound(self):
	return self.__lowerBound
    def getUpperBound(self):
	return self.__upperBound
    def printMe(self):
        print "Rounding Error: Output contains an incorrect value between  " + str(self.__lowerBound) + " and " + str(self.__upperBound)

class error:
	def __init__(self,type,arg1, arg2):
		if type = "rounding":
			self.__error = roundingError(arg1, arg2)
	def getError(self):
		return self.__error """
        
class test:
    inputString = "Input:\n"
    outputString = "Output:\n"
#   errorString = "Error:\n"
    def __init__(self, points):
	self.__inputs = []
	self.__outputs = []
#	self.__errors = []
	self.__points = points
    def getInputs(self):
	return self.__inputs
    def getOutputs(self):
	return self.__outputs
#    def getErrors(self):
#	return self.__errors
    def getPoints(self):
	return self.__points

    def newInput(self, input): #append to the list input
        self.__inputs.append(input)
    def newOutput(self, output): #append to the list output
         self.__outputs.append(output)
#    def newError(self, error):
#	self.__errors.append(error)
    def printMe(self):
	print "Worth a maximum of " + str(self.__points) + " points"
        for i in self.__inputs:
            i.printMe()
        for o in self.__outputs:
            o.printMe()
#	for e in self.__errors:
#	    e.printMe()     
            
class labDescription:
    testString = "Test:\n"
    endTestString = "/Test:\n"
    def __init__(self):
	self.__tests = []
	self.__maxPoints = 0
    
    def setMaxPoints(self,maxPoints):
	self.__maxPoints = maxPoints

    def getTests(self):
	return self.__tests

    def getTest(self,index):
	return self.__tests[index]

    def getMaxPoints(self):
	return self.__maxPoints

    def newTest(self, test): #append to the list output
        self.__tests.append(test)
    
    def printMe(self):
        for i, t in enumerate(self.getTests()):
            print "TEST #",i
            t.printMe()

def parseInput(line):
#    print line
    quoteFlag = False
    quoteString = ""
    names = []
    placeHolders = []
    count = 0
    for word in line.split():
        if word == ":":
            count += 1
            continue
        if count == 0 and quoteFlag:
                if word == "\x22":
                        quoteFlag = False
                        names.append(quoteString[:len(quoteString)-1])
			quoteString = ""
                        continue
                else:
                        quoteString += (word + " ")
                        continue
        if count == 0 and not quoteFlag:
                if word == "\x22":
                        quoteFlag = True
                else:
                        names.append(word)
        elif count == 1:
            placeHolders.append(word)
        elif count == 2:
            testValue = word
    i = input(names,placeHolders,testValue)
    return i

def parseOutput(line):
    quoteFlag = False
    quoteString = ""
    count = 0
    names = []
    for word in line.split():
        if word == ":":
                count += 1
                continue
        if count == 0 and quoteFlag:
                if word == "\x22":
                        quoteFlag = False
                        names.append(quoteString[:len(quoteString)-1])
			quoteString = ""
                        continue
                else:
                        quoteString += (word + " ")
                        print quoteString
                        continue
        if count == 0 and not quoteFlag:
                if word == "\x22":
                        quoteFlag = True
                else:
                        names.append(word)
    o = output(names)
    return o


            
"""def parseInput(line):
#    print line
    names = []
    placeHolders = []
    count = 0
    for word in line.split():
        if word == ":":
            count += 1
        elif count == 0:
            names.append(word)
        elif count == 1:
            placeHolders.append(word)
        elif count == 2:
            testValue = word
            
    i = input(names,placeHolders,testValue)
    return i 

def parseOutput(line):
    names = []
    for word in line.split():
        names.append(word)
    o = output(names)
    return o """

""" def parseError(line):
	args =[[]]
	type = ""
	count = 0
	for word in line.split():
		if count == 0:
			count += 1
			type = word
		elif word == ":":
			count += 1
		elif count == 1:
			args[0].append(word)
		elif count == 2:
			args[1].append(word)
		elif count == 3:
			args[2].append(word)
		elif count == :
			args[0].append(word)
	e = error(type,args[[]])
"""

def parsePoints(line):
	return int(line)
		
def parseFileDescriptor(descriptorPath):
    descriptString  = open(descriptorPath, 'r').readlines()
    labDescript = labDescription()
    for i, line in enumerate(descriptString):
	if i == 0:
	    labDescript.setMaxPoints(parsePoints(line))
        elif line == labDescript.testString:
            t = test(parsePoints(descriptString[i+1]))
        elif line == t.inputString:
            t.newInput(parseInput(descriptString[i+1]))
        elif line == t.outputString:
            t.newOutput(parseOutput(descriptString[i+1]))
#	elif line == t.errorString:
#		t.newError(parseError(descriptString[i+1])
        elif line == labDescript.endTestString:
	    t.printMe()
            labDescript.newTest(t)        
    labDescript.printMe()
    return labDescript



def getFunction(fileString,fName):  
    bCount = 0
    x = [0,0]
    x[0] = find(fileString, fName) #what if main is in a function name?
    #check before and after for space
    b = x[0]
    while True:
        b = getBracket(fileString,b)
        if b > 0:
            #print "found {"
            bCount += 1
        else:
            #print "found }"
            b = -b #make b positive
            bCount -= 1
        if bCount == 0:
            break
    x[1] = b
    return x

def getBracket(fileString,start): #return pos of next bracket, neg if it is }
    a = find(fileString, "{",start)
    a += 1
    b = find(fileString, "}",start)
    b += 1
    if a<b:
        return a
    if b<a:
        return -b
    
def pR(): #parses roster for {last name) , creates list of tuples (last name, file name,
    list = []
    roster = open(rosterPath, 'r' ) #open roster
    for line in roster: #read line
            t = [split(line)] #parse line for last name, placeholder for file name and sfstring. store in tuple t
            list.append(t) #add t to the list
    return list

#def makePrintsSingleLine(fileString):
#	flag = False
#	for line in fileString.splitlines():	
#			if "printf" in line:
#				if ";" in line:
#				else
					

"""def removeComment(fileString):
	lFS = fileString.splitlines()
	blockFlag = False
	for line in lFS:
		if "/*" in line.lstrip():
			blockFlag = True
			fileString = fileString.replace(line,"")
			continue
		if blockFlag:	
			fileString = fileString.replace(line,"")
			if "*/" in line.lstrip():
				return fileString,True
		if "//" in line.lstrip():
			fileString = fileString.replace(line,"")
			return fileString,True
	return fileString,False

def removeComments(fileString):
	x = removeComment(fileString)
	while x[1]:
		fileString = x[0]
		x = removeComment(fileString)
	return fileString"""



def getNextComment(fileString):
    x = [-1,-1]
    x[0] = fileString.find("//")
    if x[0]>=0:
        x[1] = fileString[x[0]:].find("\n") + x[0]-1 
        return x
    x[0] = fileString.find("/*")
    if x[0]>=0:
        x[1] = fileString[x[0]:].find("*/") +x[0]+1
    return x

def removeComments(fileString):
    #print fileString
    x = getNextComment(fileString)
    #fileString = replace(fileString, fileString[x[0]:x[1]+1],"")
    while x[0]>=0:
        fileString = fileString.replace(fileString[x[0]:x[1]+1],"",1)
        x = getNextComment(fileString)    
    return fileString


def removeAllPunct(fileString):
	for line in fileString.splitlines():
		if "printf" in line:
#			print line
			nLine = removeLinePunct(line)
			fileString = fileString.replace(line,nLine)
	return fileString

def removeLinePunct(line):
	prString = getPrintString(line)
#	print prString
	prString = prString.replace("\\n", " \\n ")
	prString = prString.replace("\\t", " \\t ")
#	print prString
	for word in prString.split():
#		print word
		if "%" in word and not "\%" in word:
			continue
		if "\\n" in word or "\\t" in word:
			continue
		else:
			nWord = removePunct(word)
			line = line.replace(word,nWord)
	return line

def removePunct(word):
	for char in list(word):
		if char in string.punctuation:
			word = word.replace(char," ")
	return word

def makePrLC(line):
	printString = getPrintString(line)
#	print printString
	nPrString = makeLowerCase(printString)
	nLine = line.replace(printString, nPrString)
	return nLine

def checkMultiLine(pos, fs):
        if pos == -1:
                return False
        nLinePos = fs.find("\n", pos)
        sCPos = fs.find(";", pos)
        if sCPos > nLinePos:
                return True
	elif fs[pos:sCPos+pos].count("\x22") > 2:
		return True
	else:
	        return False

def fixLines(pos, fs):
        sCPos = fs[pos:].find(";") + pos
        brokenPrint = fs[pos:sCPos]
        fixedNewLines = ' '.join(brokenPrint.split())
        fs = fs.replace(brokenPrint,fixedNewLines)
        return fs

def fixQuotes(pos, fs):
        sCPos = fs[pos:].find(";") + pos
        brokenPrint = fs[pos:sCPos]
        startQuote = brokenPrint.find("\x22") +1
        endQuote = brokenPrint.rfind("\x22")
        printString = brokenPrint[startQuote:endQuote]
        partialFixedPrint = printString.replace("\x22", " ")
        fixedPrint = brokenPrint.replace(printString, partialFixedPrint)
        fs = fs.replace(brokenPrint, fixedPrint)
        return fs

def fixMultiLine(pos, fs):
        fs = fixLines(pos, fs)
        fs = fixQuotes(pos, fs)
        return fs

def fixAllMultiLine(fs):
	fs = fixAllMultiLinePrints(fs)
	fs = fixAllMultiLineScans(fs)
	return fs

def fixAllMultiLineScans(fs):
        nextScanPos = 1
        scanPos = fs.find("scanf")
	if scanPos == -1:
		return fs
        scanPos += 1
        while True:
                if checkMultiLine(scanPos, fs):
#                        print "print at position " + str(printPos) + " is Multi Line"
                        fs = fixMultiLine(scanPos, fs)
                nextScanPos =  fs[scanPos:].find("scanf") + 1
                if nextScanPos == 0:
                        break
                else:
                        scanPos += nextScanPos
#                        print "Next printf is at " + str(printPos)
        return fs



def fixAllMultiLinePrints(fs):
        nextPrintPos = 1
        printPos = fs.find("printf")
        printPos += 1
        while True:
                if checkMultiLine(printPos, fs):
#                        print "print at position " + str(printPos) + " is Multi Line"
                        fs = fixMultiLine(printPos, fs)
                nextPrintPos =  fs[printPos:].find("printf") + 1
                if nextPrintPos == 0:
                        break
                else:
                        printPos += nextPrintPos
#                        print "Next printf is at " + str(printPos)
        return fs

def getPrintString(line):
        q1 = find(line, "\x22") #finds first quote
        q1 += 1 #increment to ommit first quote in format string
	q2 = find(line, "\x22", q1) #finds second quote
	while True:
		if line[q2-1] == "\x2F":
			q2 += 1
			q2 = find(line, "\x22", q2) #finds second quote
			continue
		break					
	return line[q1:q2]

def makeLowerCase(printString):
	return printString.lower()

def makeAllPrLC(fileString):
	for line in fileString.splitlines():
		if "printf" in line:
			nLine = makePrLC(line)
#			print line
#			print nLine
			fileString = fileString.replace(line,nLine)
	return fileString

def removePrints(fileString):
    for line in fileString.splitlines():
	if "%" in line:
        	continue
        else:
            if "printf" in line:
                fileString = fileString.replace(line,"")
#    print fileString
    return fileString

def removeConsoleCheck(fileString):
    pos = -5
    while True:
        pos = find(fileString, "scanf", pos+5)
#        print fileString[pos:pos+5]
        if pos == -1:
            break
        if consoleCheck(fileString, pos):
            pos1 = find(fileString, ";", pos)
            pos1 = find(fileString, "\n", pos1)
            fileString = fileString.replace(fileString[pos:pos1],"")
    return fileString


class printList:
    prList = []
    numPrints = 0
    def __init__(self, fileString):
        self.makePrintList(fileString)
    def printFN(self, fileString, lineNumb):
        for i, line in enumerate(reversed(fileString.splitlines())):
            if i < lineNumb:
                continue
            #} means skip one structure per
            #elif list of element in loop/if statement in OR MATCHES regex of loop/ifstatement starting line  
            #elif (element of listofFunctions in line return:
            match = re.search('else',line) #function name that has else in it??????
            if match:
                continue
            match = re.search(r'\s*\S+\s+\S+\s*\((\s|\S)*?\)\s*{?(\s|\S)*',line)
            if match:
                match = re.search(r"(?P<returnType>\S+) (?P<functionName>\w+)",line)
                return(match.group(2))
            match = re.search('main',line) #if main, may not have a return type.  Handle this situation
            if match:
                match = re.search(r'\s*\S+\s*\((\s|\S)*?\)\s*{?(\s|\S)*',line)
                if match:
                    match = re.search(r"(?P<functionName>\w+)",line)
                    return(match.group(1))


            
    def makePrintList(self, fileString): #append to the list input
        printPos = -6
        while True:
            printPos = find(fileString, "printf", printPos+6)
            if printPos == -1:
                break
            else:
                self.numPrints +=1
                q1 = find(fileString, "\x22", printPos) #finds first quote
                q1 += 1 #increment to ommit first quote in format string

                q2 = find(fileString, "\x22", q1) #finds second quote
                while True:
			if fileString[q2-1] == "\\":
				q2 = find(fileString, "\x22", q2)
			else:
				break		
		#print "index of quotes is  " + str(q1) + " and " + str(q2) + str(fileString[q1-1]) + str(fileString[q2])
                printString = fileString[q1:q2] #creates a substing for the format spec
                lineCount = count(fileString,"\n")
                printPosN = count(fileString,"\n", 0,q1)
                printPosNInv = lineCount - printPosN
                functName = self.printFN(fileString,printPosNInv)
                t = printPosN, functName, printString
                self.prList.append(t)

    def clearPrintList(self):
	self.prList[:] = []
	self.numPrints = 0
	
    def printMe(self):
        for pr in self.prList:
            print pr       
            
sList = pR() #list of students
fileDescript = parseFileDescriptor(descriptorPath)
aList = [] #list of absent students
unmatchedAssignmentsList = []
#gCount = 0
#sem = threading.Semaphore()

#change to delete console check!
def scanSearch(fileString):
    list = []
    lineCount = count(fileString,"\n")
    #start at position 0 search file for scanf
    scanPos = -5
    while True: #while there are still more scanfs						
            scanPos = find(fileString, "scanf", (scanPos+5) ) #look for next scanf, starting right after prev	

            if scanPos == -1: #if there are no more scanfs, 
                    break #stops searching
            else: #if there are more scanfs,
                    #if consoleCheck(fileString, scanPos): #if the current scanf should not be considered
                            #print "scanf at position " + str(scanPos) + " is a throwaway"
                            #print "there is a console check!"
                            #need to handle this when generating the script
                            #continue #skip it
                    #else: #if it should be counted
                            #print "scanf at position " + str(scanPos) + " is valid" #prints position of found scanf
                q1 = find(fileString, "\x22", scanPos) #finds first quote
                q1 += 1 #increment to ommit first quote in format string
                q2 = find(fileString, "\x22", q1) #finds second quote
                #print "index of quotes is  " + str(q1) + " and " + str(q2) + str(fileString[q1-1]) + str(fileString[q2])
                format = fileString[q1:q2] #creates a substing for the format specs
                scanPosN = count(fileString,"\n", 0,scanPos)
                scanPosNInv = lineCount - scanPosN
                functName = scanFN(fileString,scanPosNInv)
                t = scanPosN, functName, format #creates a tuple of position and format string
                list.append(t) #adds it to a list
                            #print "the format specifier associated with this scanf is " + format
    return list

def scanFN(fileString, lineNumb):
    bFlag = 0
    for i, line in enumerate(reversed(fileString.splitlines())):
        if i < lineNumb:
            continue
        #} means skip one structure per, elif list of element in loop/if statement in OR MATCHES regex of loop/ifstatement starting line, elif (element of listofFunctions in line return:
        """match = re.search(r'\s*{\s*\n',line)
        if match: #single bracket
            print line,"yes"
            bFlag = 1
            continue
        match = re.search(r'\s+',line) #if blank line ignore
        #print line, "yes"
        if match: #single bracket
            continue
        else:
            bFlag = 0
        match = re.search('else',line) #function name that has else in it??????
        if match:
            continue
        if bFlag == 1
            match = re.search(r'\s*\S+\s+\S+\s*\((\s|\S)*?\)\s*(\s|\S)*',line)
        else:"""
        match = re.search(r'\s*\S+\s+\S+\s*\((\s|\S)*?\)\s*{?(\s|\S)*',line)
        if match:
            match = re.search(r"(?P<returnType>\S+) (?P<functionName>\w+)",line)
            return(match.group(2))
        match = re.search('main',line) #if main, may not have a return type.  Handle this situation
        if match:
            match = re.search(r'\s*\S+\s*\((\s|\S)*?\)\s*{?(\s|\S)*',line)
            if match:
                match = re.search(r"(?P<functionName>\w+)",line)
                return(match.group(1))


        
def consoleCheck(fileString, pos): #determines any scanfs that should be thrown away, handles blanks, newlines, comments and extra brackets
    bCount = 0
    pos = find(fileString, ";", pos) #get location of ';' associated with last scanf
    pos += 1
    while True:
            #print "Checking " + str(fileString[pos])
            #if fileString[pos]== ' ' or fileString[pos] == '\n' or fileString[pos] == '\r' or fileString[pos] == '\t': #skips characters that do not represent c code
            if fileString[pos].isspace():
                    pos = (pos + 1)
                    #print "pos is now " + str(pos)
                    continue
            elif fileString[pos]=='{': #skips { and will continue, also looking for matching }
                    pos = (pos + 1)
                    bCount = (bCount + 1)
                    continue
            elif fileString[pos]=='/' and fileString[pos+1]=='/': #skips //, goes to new line and continues
                    pos = find(fileString, "\n", pos)
                    pos = (pos + 1)
                    continue
            elif fileString[pos]=='/' and fileString[pos+1]=='*': #skips comment blocks
                    pos = find(fileString, "*/", pos)
                    pos = (pos + 3)			
                    continue
            elif fileString[pos]=='}' and bCount > 0: #found matching } to an extra {
                    pos = (pos + 1)			
                    bCount = (bCount - 1)
                    continue
            elif fileString[pos] =='}' and bCount == 0: # } directly follows scanf
                    return True
            else:
                    return False
                
def matchStudent(n): #matches students to program currently bSeing graded, returns index of that student
    #print sList
    #print "attempting to match " + n
    for index, s in enumerate(sList): #for each list of student descriptors
            #print n + "and " + s[0]
            if len(s) > 1: #skips student if they are already assigned
                    #print "skipping " +s[0] + " already matched"
                    continue
            nameString = "".join(s[0])
            if nameString in n or nameString.upper() in n or nameString.lower() in n:
                    return index
            fileString = open(assignmentsPath+n, 'r').read() #open file, read entire file
            pos=find(fileString,nameString)
            if (find(fileString,nameString)>0 and not fileString[pos+len(nameString)].isalpha() and not fileString[pos-1].isalpha()): #matched via file name
                return index
            pos=find(fileString,nameString.upper())
            if (find(fileString,nameString.upper())>0 and fileString[pos+len(nameString)].isalpha() and fileString[pos-1].isalpha()): #matched via file name
                    return index
            pos=find(fileString,nameString.lower())
            if (find(fileString,nameString.lower())>0 and fileString[pos+len(nameString)].isalpha() and fileString[pos-1].isalpha()): #matched via file name
                    return index
    return -1 #return failure
    
def grade(s, index):
    results = []
#    global gCount, sem
#    print "grading", s
    fileString = open(assignmentsPath+s, 'r').read()
#    print "0"
#    print fileString
    fileString = removeComments(fileString)
#    print "0.1"
#    print fileString
    fileString = fixAllMultiLine(fileString)
#    print "0.2"
#    print fileString
    fileString = makeAllPrLC(fileString)
    fileString = removeAllPunct(fileString)
#    print "1"    
#    print fileString
    prList = printList(fileString)
#    print "2"
#    print prList.prList
    fileString = removeConsoleCheck(fileString)
#    print fileString
    scanList = scanSearch(fileString)
    print "3"
    print scanList
#    fileString = removePrints(fileString)
#    print fileString
    if len(scanList) == 0 or prList.numPrints == 0:
	return 0
    orderedScanList = orderScanString(fileString,scanList)
    orderedPrList = orderPrList(fileString,prList)
    newFS = assignmentsPath+"n"+s
    f = open(newFS, 'w+')
    f.write(fileString)
 #   print "4"
 #   print fileString
    print "5"
    print orderedScanList
    print "6"
    print orderedPrList
    for i, test in enumerate(fileDescript.getTests()):
#	test.printMe()
	matchList = match(orderedScanList,orderedPrList,test.getInputs())
	if matchList == None:
#		deleteFile(newFS)
#	fileString = ""
		prList.clearPrintList()
#	scanList = None
#	newFS = ""
#	f = None
#		print sList[index], "No matches found for test " + str(i)
		results.append(False)
	else:
#		print "match found",
#		test.printMe()
		makeScript(newFS,matchList, test.getInputs())
#		print "script made"
		f = open("./script.sh").read()
		print f
		runScript("script.sh")
		rS = open("./output.txt").read()
		print rS
#		print "script was run"
		outputString = open("./output.txt", 'r').read()
		if checkTest(outputString, test):
			deleteFile("./output.txt")
			deleteFile("./script.sh")
#			deleteFile(newFS)
#		fileString = ""
#			prList.clearPrintList()
#		scanList = None
#		newFS = ""
#		f = None
			print sList[index], "test " + str(i) + " passed"
			results.append(True)
			continue

		else:
#			deleteFile(newFS)
			deleteFile("./output.txt")
			deleteFile("./script.sh")
#		fileString = ""
#			prList.clearPrintList
#		scanList = None
#		newFS = ""
#		f = None
			print sList[index], "test " + str(i) +  " failed"
			results.append(False)
    prList.clearPrintList()
    deleteFile(newFS)
    score = calculateGrade(results)
    return score
    #print orderedScanString
    
    #for i, t in enumerate(fileDescript.tests): #for each test
    #m = match(fileDescript.tests[0],orderedScanString,orderedPrList)
    #if m:
        #string = "gcc "+newFS+"\n./a.out >> "+index+"o.txt << EOF\n"
        #5 5\n
        #string +="EOF\nexit"
            #makeScript(string)
    #create all tests in their own script!
    #then create a master script that runs all the other smaller scripts
    #print "1",orderedScanString
    #print "2",orderedPrList
   
        
 #   sem.acquire()
 #   gCount += 1
 #   sem.release()

def deleteFile(fileName):
	os.system("rm " + fileName)
	
def makeScript(fileName,matchList,inputs):
    #add script passed here to list of scripts
    #when master script is made
    #print out string that is going to be passed to checker
    #[[student name, outputfile name], [expected values]] q
    #takes argument that is scanf descriptor
    #>mailx -s "assignment grade" tuc44548@temple.edu < t.py
    """generates script to grade the file
    1. gcc [filename]
    2. ./a.out (redirect output to a text file)
    3. simulate user input to match scanf
      gcc test.c
   ./a.out >> output.txt << EOF
    55
    EOF
    4. repeat either internally via program (y/n loop) or externally (repeat ./a.out)
    >>
    5. parse text file to grade
    """
    """FILE MUST BE CREATED IN UNIX"""
    
    #string = "gcc\x20DoyleEnglish.c\n./a.out\x20>>\x20output.txt\x20<<\x20EOF\n5\x205\nEOF\nexit"
    string = "gcc -lm "+ fileName + "\n./a.out >> output.txt << EOF\n"
    for m in matchList:
        string = string + str(inputs[m[0]].getTestValue()) + "\n"
    string = string + "EOF\nexit"
    f = open(r'./script.sh','w+')
    f.write(string) # ... etc.
    #sList[0][1][0]

def orderScanString(fileString, scanString):
    newList = []
    b = [] #main start and end characters
    b = getFunction(fileString,"main")
    #print fileString[b[0]:b[1]]
    startLine = count(fileString[0:b[0]],"\n") #start line of main
    endLine = count(fileString[0:b[1]],"\n") #end line of main

    #print scanString
    #problem, change +.01 to + (linenumber in function / # of lines in function) using getFunction
    j = 0;
    prev = scanString[0][1]
    #print scanString
    for e in scanString:
        if e[1] == "main":
            newList.append(e)
            continue
        else:
            for i, line in enumerate(fileString.splitlines()):
                if i < startLine or i > endLine:
                    continue
                else:
                    #print e[1]
                    if e[1] in line:
                        if e[1] != prev:
                            j = 0
			k = i+j
#                        k = round(k,2)
                        f = k, e[1], e[2]
                        j += .01
                        #f[0] = round(f[0],2)
			newList.append(f)
                        prev = e[1]
    newList.sort()
    return newList

def match(ss,ps,inputs):
#    count = True
    numMatches = 0
    matchList = []
    inputSkip = []
    #print inputs
    #print ss
    #print len(ss)
    numPH = 0
    for input in inputs:
        x = False
        inputSkip.append(x)
    for sf in ss:
#	sf[2] = str(sf[2]).replace("%", " %")
        placeHolders = str(sf[2]).replace("%", " %").split()
#	print placeHolders
        numPH += len(placeHolders) #min matches
#print numPH
#    print "num inputs", len(inputs), "num PH", numPH
    if len(inputs) != numPH:
	return None
    for k, sf in enumerate(ss):
        #if count:
            #print "this is the scanf", sf
        placeHolders = str(sf[2]).replace("%", " %").split()
#        if count:
#            print "this is the list of placeholders", placeHolders
        for i, placeHolder in enumerate(placeHolders):
            skip = False
            #if count:
                #print "This is a placeholder", placeHolder
            pr = getClosestPrint(sf[0], ps)
            #if count:
                #print "This is a print statement", pr
            for j, input in enumerate(inputs):
                if skip:
                    continue
                #if count:
                    #print "below is an input"
                    #input.printMe()
                for dataType in input.getDataTypes():
                    if skip:
                        continue
                    if dataType == placeHolder:
#                        if not inputSkip[j]:
#				print "attempting to match", placeHolder, pr, input.getNames()
                        m = matchInput(placeHolder,pr,input) #true if match, pr is index of closet pr
#                        count = False
                	if m != None and not inputSkip[j]:
                    		inputSkip[j] = True
                        	skip = True
                        	numMatches += 1
                    		x=j,k + (i*.1)
                    		matchList.append(x)#input name and input order
 #                   		print "found match", "number of matches:", numMatches
                    		if numMatches == numPH:
                        		return matchList
    #return None
    return None
                
def matchInput(pH,prS,input):
#    print "the names of the input are ", input.names
    t1 = False
    #print prS
    #print pH
    for word in prS.split():
        #print word
        for name in input.getNames():
            if word == name or word == name.lower() or word == name.upper():
                t1 = True
#                print "FOUND MATCH"
#                print pH, prS
#                print "FOUND MATCH"
#                input.printMe()
                return pH
     #           print "Found 1"
    if not t1:
#        print "no match"
        return None
#check if mapping is 1 to 1

def getClosestPrint(lineNumb,orderedPrList):
    for i, pr in enumerate(orderedPrList):
	if i+1 == len(orderedPrList):
		return pr[2]
        if orderedPrList[i+1][0]>lineNumb:
            return pr[2]
    return None

def orderPrList(fileString, prList):
    newList = []
    b = [] #main start and end characters
    b = getFunction(fileString,"main")
    #print fileString[b[0]:b[1]]
    startLine = count(fileString[0:b[0]],"\n") #start line of main
    endLine = count(fileString[0:b[1]],"\n") #end line of main
    #prList.printMe()
    #problem, change +.01 to + (linenumber in function / # of lines in function) using getFunction
    j = 0
    prev = prList.prList[0][1]
    for e in prList.prList:
        if e[1] == "main":
            newList.append(e)
            continue
        else:
            for i, line in enumerate(fileString.splitlines()):
                if i < startLine or i > endLine:
                    continue
                else:
                    if e[1] in line:
                        if e[1] != prev:
                            j = 0
			k = i + j
                        #k = round(i+j,2)
                        f = k, e[1], e[2]
                        j += .01
                        newList.append(f)
                        prev = e[1]
    newList.sort()
    return newList




"""def checkTests(fileString, labD):
        for t in labD.getTests():
                if checkTest(fileString, t):
                        continue
                else:
                        return False
        return True"""

def checkTest(fileString, test):
        for output in test.getOutputs():
                if checkOutput(fileString, output):
			continue
		else:
			return False
        return True

def checkOutput(fileString, output):
        for search in output.getsearchStrings():
                if checkSearch(fileString, search):
                        return True
        return False

def checkSearch(fileString, search):
        if search in fileString:
                return True
        else:
                return False


def runScript(scriptName):
        os.system("sh " + scriptName)


def calculateGrade(results):
    totalPoints = 0
    for i, result in enumerate(results):
	if result:
		totalPoints += fileDescript.getTest(i).getPoints()		
		print "Test Number ", i, " passed.  Student awarded " + str(fileDescript.getTest(i).getPoints()) + " points"
	else:
		print "Test Number ", i, " failed.  Student awarded 0 points"
    return max(min(int(fileDescript.getMaxPoints()),totalPoints),60)
    
def main():
    #print threading.activeCount()
    files = os.listdir(assignmentsPath)#get list of files
    for n in files: 
        if (".cpp" in n):
            os.rename(assignmentsPath+n, assignmentsPath+n.replace(".cpp", ".c"))
            n = n.replace(".cpp", ".c")
            #check for .cppx first, if true rename to .c
        if not(".c" in n): #skip any file that isnt C code
            continue
        index = matchStudent(n) #match file to index of student in array
        if index >= 0:
            fileName = []
            fileName.append(n) 
            sList[index].append(fileName) #combine student name and file name
        else:
            unmatchedAssignmentsList.append(n)

    for i, s in enumerate(sList): #prints who is missing which assigment and removes them from student list
            if len(s) == 1:
                    print ''.join(s[0]) + " is missing current graded assigment"
                    aList.append(s)
                    sList.pop(i)                                        
    print "submitted student list:"
    for s in sList:
            print s
    if len(aList) == 0:
        print "no absent students"
    else:        
        print "absent student list:"        
        for a in aList:
                print a

    if len(unmatchedAssignmentsList) == 0:
        print "no unmatched students"
    else:
        print "unmatched assignments list:"
        for u in unmatchedAssignmentsList:
                print u
    #start multithreading version of grade


#   for i, s in enumerate(sList):
    grade(sList[12][1][0],12)
"""    for i, s in enumerate(sList):
#	if i>13:
#		continue
	print "grading", s
	score = grade(s[1][0],i)
	s.append(score)
	if score > 0:
		print s, str(score)+"/"+str(fileDescript.getMaxPoints())
	else:
		print s, "Needs human review"

    for s in sList:
	print s """
main()

