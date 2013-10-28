import sublime, sublime_plugin, string

class Javadoc(object):

    indentationLevel = 0
    hasReturnType = False
    returnType = ""
    hasInputTypes = False
    inputTypes = []
    charactersAdded = 0
    doNotGenerate = False


    def __init__(self, indentation_level=None, methodSignature=None):
        if indentation_level is None:
            indentation_level = []
        self.indentationLevel = indentation_level
        self.inputTypes = []
        if methodSignature is None:
            methodSignature = ''
        else:
            self.parseMethodSignature(methodSignature)


    #creates javadoc string and returns it
    def createMethodJavadoc(self):
        if self.doNotGenerate:
            self.doNotGenerate = False
            return ''
        else: 
            indents = " " * 4 * self.indentationLevel
            #output = indents + "/**" + "\n"
            output = "/**" + "\n"
            output = output + (indents + " *" + "\n")*2
            #output = output + indents + " *" + "\n"
            if self.hasInputTypes:
                for inputType in self.inputTypes:
                    output = output + "{0} * @param {1}\n".format(indents, inputType)
            if self.hasReturnType:
                output = output + "{0} * @return \n".format(indents)
            output = output + indents + " */\n" + indents
            #self.returnType = ""
            self.charactersAdded = len(output)
            return output
    
    def createClassJavadoc(self):
        output = """/**\n *\n * @author\n * @version\n */\n"""
        return output

    #called in the constructor to fill object with javadoc relevant variables 
    def parseMethodSignature(self, sig):
        print sig
        inputListOriginal = sig[ sig.index("(")+1 : sig.index(")")].split(",")
        wordsBeforeInputList = sig[ : sig.index("(")].split(" ")
        if "main" in wordsBeforeInputList:
            self.doNotGenerate = True
            return
        self.doNotGenerate = False
        print wordsBeforeInputList
        #if we have inputs, find them
        if inputListOriginal[0] != '':
            inputTypes = []
            self.hasInputTypes = True
            for inputSig in inputListOriginal:
                self.inputTypes.append( inputSig.strip().split(" ")[1] )
        #if there is no return type OR if it's a contructor
        if ("void" in sig) or (len(wordsBeforeInputList)<=2):
            self.hasReturnType = False
        else:
            self.hasReturnType = True
            #word before method name is always return type
            self.returnType = wordsBeforeInputList[-2]

class JavadocCommand(sublime_plugin.TextCommand):

    def determineIndentation(self,region):
        (row, col) = self.view.rowcol(region.begin())  
        indent_region = self.view.find('^\s+', self.view.text_point(row, 0))  
        indent_level = len(self.view.substr(indent_region))/4
        return indent_level

    def alreadyCommented(self,region):
        (row,col)= self.view.rowcol(region.begin())
        previous_line = self.view.line(self.view.text_point(row-1,0))
        print self.view.substr(previous_line)
        if "*/" in self.view.substr(previous_line):
            return True
        else:
            return False


    def run(self, edit):
        #check if it's a java file
        #fileName = self.view.file_name()[-4:]
        classSignature = self.view.find("""(public|private|protected) (abstract )?(class|interface|enum)""",0)
        #indentation_level = self.determineIndentation(classSignature)
        #maybe do this better?
        javadocer = Javadoc()
        self.view.insert(edit,classSignature.begin(), javadocer.createClassJavadoc())
        startSearchPoint = 0
        foundPublicsCount = self.view.find_all("public.*\\)")
        #use the [region] as a counter of how many comments we're inserting
        for methodSignatures in foundPublicsCount:
            #find from startSearchPoint because everytime we insert comments,
            #all characters move so we have to continually keep searching for
            #the next method signature
            methodSignature = self.view.find("public.*\\)", startSearchPoint)
            methodSignatureString = self.view.substr(methodSignature)
            indentation_level = self.determineIndentation(methodSignature)
            javadocer = Javadoc(indentation_level, methodSignatureString)
            if not self.alreadyCommented(methodSignature):
                self.view.insert(edit,methodSignature.begin(),javadocer.createMethodJavadoc())
            startSearchPoint = methodSignature.end()+javadocer.charactersAdded
            

    
