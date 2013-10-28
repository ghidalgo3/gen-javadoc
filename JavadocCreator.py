import sublime, sublime_plugin
from Javadoc import *

class JavadocCommand(sublime_plugin.TextCommand):

    def determineIndentation(self,region):
        (row, col) = self.view.rowcol(region.begin())  
        indent_region = self.view.find('^\s+', self.view.text_point(row, 0))  
        indent_level = len(self.view.substr(indent_region))/4
        return indent_level

    def alreadyCommented(self,region):
        (row,col)= self.view.rowcol(region.begin())
        previous_line = self.view.line(self.view.text_point(row-1,0))
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
        if not self.alreadyCommented(classSignature):
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
            

    
