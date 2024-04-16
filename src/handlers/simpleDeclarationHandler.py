import re
import service.generalizeService
from grammars.CPP14Parser import *
from antlr4.tree.Tree import TerminalNodeImpl

from handlers.TerminalNodeHandler import TerminalNodeHandler


class SimpleDeclarationHandler:

    def __init__(self, generalize_flag, store):
        self.flag_attribution = False
        self.generalizer: service.generalize.GeneralizeService = generalize_flag
        self.store = store
        self.regex = r'^[a-zA-Z_]\w*$'



    def visit2( self,child):
        from grammars.CPP14Parser import CPP14Parser

        if type(child) == TerminalNodeImpl: #if its a terminal (leaf)
            return [self.generalizeVar(child.getText())]
        if type(child) == CPP14Parser.InitializerContext: #if it is an initializer, we don't care. just get the tokens, there is no processing techniques to apply.
                return self.addTokensToStore(child)
        elif child.children:
            tokens = []
            for child2 in child.children:
                a = self.visit2(child2)
                if len(a) > 0:
                    tokens = tokens + a
            return tokens

    def addTokensToStore(self,child):
        if type(child) == TerminalNodeImpl: #if its a terminal (leaf)
            return [TerminalNodeHandler(generalizer=self.generalizer).handle(child.getText())]
        elif child.children:
            tokens = []
            for child2 in child.children:
                a = self.addTokensToStore(child2)
                if len(a) > 0:
                    tokens = tokens + a
            return tokens
     # Enter a parse tree produced by CPP14Parser#simpleDeclaration.
    def enterSimpleDeclaration( self, ctx:CPP14Parser.SimpleDeclarationContext):
        tokens = []
        if ctx.declSpecifierSeq():
            tokens = self.addTokensToStore(ctx.declSpecifierSeq())
            for child in ctx.initDeclaratorList().initDeclarator(): #for each variable that we will declare
                tk = self.visit2(child)
                if tk:
                    tokens = tokens  +tk + [","]

            tokens.pop() #lets remove the exceding comma due to the line above.

            self.store.addTokens(list(tokens))
            self.store.addTokens(list(self.addTokensToStore(ctx.children[-1])))
            return None
        else: #its not a variable declaration (grammar bug)
            for child in ctx.children:
                tk = self.addTokensToStore(child)
                if tk:
                    tokens = tokens + tk
            self.store.addTokens(list(tokens))
            return None


    def is_valid_variable_name(self, name):
        return not (re.match(self.regex, name) == None)
    def generalizeVar(self, name):
        name = TerminalNodeHandler(self.generalizer).handle(name)
        if name == "=" or name == "," or not self.is_valid_variable_name(name):
            return name
        return self.generalizer.translateVariable(name)

