from antlr4.tree.Trees import Trees
import service.generalizeService
from grammars.CPP14Parser import *
from antlr4.tree.Tree import TerminalNodeImpl
import re
class FunctionDeclarationHandler:
    '''
    Class that handles the "declaration" type of nodes.
    Note that variable declarations, despite being under a "declaration" node we don't want to use this class to handle variable declarations.
    This is due to the grammar error of defining parent nodes of function calls as variable declarations type of nodes.
    '''

    def __init__(self, generalizer, store, rules):
        self.flag_attribution = False
        self.generalizer: service.generalize.GeneralizeService = generalizer
        self.rule_names = rules
        self.store = store

    def visit_function_name(self, child):
        '''
        Function that visits a tree branch related to the function name.
        In the example blow, the aim of this function is to visit the "declarator" branch.
        The function declaration subtree has always 3 branches: the declSpecifierSeqm where the function return type is specified; the declarator branch, where the function name and paramterers are defined;
        and the "functionBody", where the function code is located.
        . . declaration
        . . . functionDefinition
        . . . . declSpecifierSeq
        . . . . . declSpecifier
        . . . . . . typeSpecifier
        . . . . . . . trailingTypeSpecifier
        . . . . . . . . simpleTypeSpecifier
        . . . . . . . . . [@3,206:208='int',<45>,16:0]
        . . . . declarator
        . . . . . pointerDeclarator
        . . . . . . noPointerDeclarator
        . . . . . . . noPointerDeclarator
        . . . . . . . . declaratorid
        . . . . . . . . . idExpression
        . . . . . . . . . . unqualifiedId
        . . . . . . . . . . . [@4,210:213='main',<132>,16:4]

                                FunctionDefinition
                                        |
                        ________________|________________
                        |               |                |
                declSpecifierSeq    declarator        functionBody
                   (return type)        |              (function code)
                                    pointerDeclarator
                                        |
                                    noPointerDeclarator
                        ________________|____________________________
                        |               |                           |
                noPointerDeclarator   parametersAndQualifiers       functionBody
                             ^
                            |
                we are visiting this branch. The last node (terminal node) will be the function name.
        '''
        if type(child) == CPP14Parser.ClassNameContext:
            self.store.addToken(child.getText())
        elif type(child) == CPP14Parser.ParametersAndQualifiersContext:
            self.visit_argument_declaration(child) # for the case we have functions like func(par1, par2)(par2){}
        elif type(child) == TerminalNodeImpl:  # if its a terminal (leaf)
            self.store.addToken(self.generalizeFunction(child.getText()))

        else:
            for child2 in child.children:
                self.visit_function_name(child2)

    def visit_argument_declaration(self, child):
        '''
        Function that visits the sub-tree branch related to function's parameter declaration.

                            FunctionDefinition
                                        |
                        ________________|________________
                        |               |                |
                declSpecifierSeq    declarator        functionBody
                   (return type)        |              (function code)
                                    pointerDeclarator
                                        |
                                        |
                                    noPointerDeclarator
                        ________________|____________________________
                        |               |                           |
                noPointerDeclarator   parametersAndQualifiers       functionBody
                                            ^
                                            |
                we are visiting this branch. The terminal nodes with the tye "unqualifiedId" will be parameter names.
        '''

        if type(child) == CPP14Parser.UnqualifiedIdContext and not (type(child) == CPP14Parser.ClassNameContext):  # if its a terminal (leaf)
            self.store.addToken(self.generalizer.translateVariable(child.getText()))
        elif type(child) == TerminalNodeImpl:
            self.store.addToken(child.getText())
        else:
            for child2 in child.children:
                self.visit_argument_declaration(child2)

    def visit_declarator_branch(self, child):
        '''
                Function that visits the "declarator" branch. this function will just decide when its time to call the functions that handles the function and parameter names.

                                    FunctionDefinition
                                                |
                                ________________|________________
                                |               |                |
                        declSpecifierSeq    declarator        functionBody
                           (return type)        |              (function code)
                                            pointerDeclarator
                                                |
                                                |
                                            noPointerDeclarator
                                ________________|__________________________
                                |                                          |
                        noPointerDeclarator                     parametersAndQualifiers

                '''

        if type(child) == CPP14Parser.NoPointerDeclaratorContext:
            self.visit_function_name(child.noPointerDeclarator())
            self.visit_argument_declaration(child.parametersAndQualifiers())
        elif type(child) == TerminalNodeImpl:  # if its a terminal (leaf)

                self.store.addToken(child.getText())
        else:
            for child2 in child.children:
                self.visit_declarator_branch(child2)
    def visit(self, child):
        '''
            Function that visits the "FunctionDefinition" branch.

                                           FunctionDefinition
                                                       |
                                       ________________|________________
                                       |               |                |
                               declSpecifierSeq    declarator        functionBody
                                  (return type)        |              (function code)
                                                   pointerDeclarator
                                                       |
                                                       |
                                                   noPointerDeclarator
                                       ________________|__________________________
                                       |                                          |
                               noPointerDeclarator                     parametersAndQualifiers
                                (function name)                             (parameters)


                       '''
        from grammars.CPP14Parser import CPP14Parser

        if type(child) == CPP14Parser.DeclaratorContext:
            self.visit_declarator_branch(child)

        elif type(child) == TerminalNodeImpl:  # if its a terminal
            self.store.addToken(child.getText())
        elif child.children:
            for child2 in child.children:
                self.visit(child2)


        # Enter a parse tree produced by CPP14Parser#simpleDeclaration.
    def enterFunctionDeclaration(self, ctx: CPP14Parser.FunctionDefinitionContext):

            for child in ctx.children:
                if Trees.getNodeText(child, self.rule_names) == "functionBody":
                    return child #we just want to parse the function definition. Not the function body
                else:
                    self.visit(child)

            return None

    def generalizeFunction(self, name):
        if re.match(r"^[a-zA-Z0-9_]+",name) is not None:
            return self.generalizer.translateFunction(name)
        return name