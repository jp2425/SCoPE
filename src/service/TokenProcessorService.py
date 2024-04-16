import CustomVisitor
from errors.ParserErrorHandler import ParserErrorHandler
from grammars.CPP14Lexer import *
from grammars.CPP14ParserListener import *
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Trees import Trees
from grammars.CPP14Parser import CPP14Parser

from store.tokenStore import TokenStore
from service.generalizeService import GeneralizeService
import traceback
#import ray
class TokenProcessorService:
    """
    Class to process code, representing it as token sequences.
    """

    def __init__(self, store:TokenStore, generalizer:GeneralizeService):
        self.generalizer = generalizer
        self.store:TokenStore = store


    def dump(self, node, depth=0, ruleNames=None):
        depthStr = '. ' * depth
        if isinstance(node, TerminalNodeImpl):
            print(f'{depthStr}{node.symbol}')
        else:
            print(f'{depthStr}{Trees.getNodeText(node, ruleNames)}')
            for child in node.children:
                self.dump(child, depth + 1, ruleNames)
    def process( self,source, try_recover_from_errors = False):

        try:
            lexer = CPP14Lexer(input=InputStream(source))
            parser = CPP14Parser(CommonTokenStream(lexer))
            parser.removeErrorListeners()
            lexer.removeErrorListeners()
            if not try_recover_from_errors:
                parser._listeners = [ParserErrorHandler()]

            tree = parser.translationUnit()

            #self.dump(tree, ruleNames=parser.ruleNames)
            #exit(1)
            a = CustomVisitor.Visitor(self.generalizer, self.store)

            a.visit(tree, parser.ruleNames)
            return a.getTokens()
        except Exception:
            #print(traceback.format_exc())
            return None

    '''@ray.remote
    def process_parallel( source):
        store = TokenStore()
        from service.renameStrategies.minifyReplacement import MinifyReplacement

        repStrat = MinifyReplacement()
        generalizer = GeneralizeService(repStrat, generalize_strings=False)
        try_recover_from_errors = False
        try:
            lexer = CPP14Lexer(input=InputStream(source))
            parser = CPP14Parser(CommonTokenStream(lexer))
            if not try_recover_from_errors:
                parser._listeners = [ParserErrorHandler()]

            tree = parser.translationUnit()

            # self.dump(tree, ruleNames=parser.ruleNames)
            # exit(1)
            a = CustomVisitor.Visitor(generalizer, store)
            a.visit(tree, parser.ruleNames)
            return a.getTokens()
        except Exception:
            print(traceback.format_exc())
            return 'None' '''
