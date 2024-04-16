from antlr4.error.ErrorListener import ErrorListener

class ParserErrorHandler( ErrorListener ):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        #print (str(line) + ":" + str(column) + ": sintax ERROR, ")
        #print ("Terminating Translation")
        raise Exception((str(line) + ":" + str(column) + ": sintax ERROR, "))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        #print ("Ambiguity ERROR, " )
        #raise Exception("Ambiguity ERROR, ")
        # see: https://www.antlr.org/api/Java/org/antlr/v4/runtime/ANTLRErrorListener.html
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        #print ("Attempting full context ERROR, ")
        #raise Exception("Attempting full context ERROR, " )
        # see: https://www.antlr.org/api/Java/org/antlr/v4/runtime/ANTLRErrorListener.html
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        #print ("Context ERROR, " )
        #raise Exception("Context ERROR, " )        # see: https://www.antlr.org/api/Java/org/antlr/v4/runtime/ANTLRErrorListener.html
        pass