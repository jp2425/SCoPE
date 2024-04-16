import service.generalizeService
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Trees import Trees
from handlers.functionDeclarationHandler import FunctionDeclarationHandler
from handlers.TerminalNodeHandler import TerminalNodeHandler
from handlers.simpleDeclarationHandler import SimpleDeclarationHandler
from store.tokenStore import TokenStore


class Visitor:
    def __init__(self, generalizer: service.generalizeService, store:TokenStore):
        self.tokens = []
        self.generalizer = generalizer
        self.store = store

    def dump(self,node, depth=0, ruleNames=None):
        depthStr = '. ' * depth
        if isinstance(node, TerminalNodeImpl):
            print(f'{depthStr}{node.symbol}')
        else:
            print(f'{depthStr}{Trees.getNodeText(node, ruleNames)}')
            for child in node.children:
                self.dump(child, depth + 1, ruleNames)

    def getTokens(self):
        return self.store.getTranslatedTokens(self.generalizer)

    def visit(self, node, ruleNames, control = 0):
        if isinstance(node, TerminalNodeImpl):
            text = TerminalNodeHandler(self.generalizer).handle(node.getText())
            self.store.addToken(text)
        elif control == 1: # to avoid infinite loop
            for child in node.children:
                self.visit(child, ruleNames, control=0)
        else:
            tk = self.handlerSelector(node,ruleNames)
            if tk:
                self.visit(tk, ruleNames, control = 1)

    def handlerSelector(self, node, ruleNames):
        '''
        Register here the handlers for specific types of nodes.
        :returns
            - None: No handler handles that node
            - [tree]: the subtree that was not parsed.
        '''

       # if Trees.getNodeText(node, ruleNames) == "primaryExpression":

        if Trees.getNodeText(node, ruleNames) == "simpleDeclaration":
            return SimpleDeclarationHandler(self.generalizer, self.store).enterSimpleDeclaration(node)
        elif Trees.getNodeText(node, ruleNames) == "functionDefinition":
            return FunctionDeclarationHandler(self.generalizer, self.store, ruleNames).enterFunctionDeclaration(node)
        else: #if there is no handler, lets visit the childs.
            if node.children:
                for child in node.children:
                    self.visit(child, ruleNames)
        return None
