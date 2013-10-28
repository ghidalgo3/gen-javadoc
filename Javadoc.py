import string

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
