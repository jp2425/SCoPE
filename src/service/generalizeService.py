from service.renameStrategies.replacementStrategy import ReplacementStrategy


class GeneralizeService(object):
    _instance = None

    _blacklist_function = [  # function names that we don't want to generalize (like the main function)
        "main"
    ]

    def __init__(self, replacementStrategy: ReplacementStrategy, generalize_functions=True, generalize_vars=True,
                 generalize_strings=False,
                 generalize_classes=False):

        self.replacementStrategy = replacementStrategy
        self.dictionary = {}
        self.generalize_functions = generalize_functions
        self.generalize_vars = generalize_vars
        self.generalize_strings = generalize_strings
        self.generalize_classes = generalize_classes

    def _getFunctionName(self):
        """
        Gets the function name to be used in generalization.
        We may have multiple strategies to name functions/variables
        """

        return self.replacementStrategy.getFunctionName()

    def _getVariableName(self):
        """
        Gets the function name to be used in generalization.
        We may have multiple strategies to name functions/variables
        """

        return self.replacementStrategy.getVariableName()

    def translateLiteral(self, token):
        """
        Function used to translate strings.
        Returns the string replacer or the token.
        """

        if not self.generalize_strings:
            return token
        if (str(token).startswith("\"") or str(token).startswith("\'")) and self.generalize_strings:
            return self.replacementStrategy.getStringReplacer()
        return token

    def translateFunction(self, name):
        if not self.generalize_functions or (
                name in self._blacklist_function):  # some function names we may not want to replace
            return name

        self.dictionary[name] = self._getFunctionName()
        return name  # self._getFunctionName()
    def sortDict(self):
        test_dict_list = list(self.dictionary.items())
        test_dict_list.sort(key=len,reverse=True)

        # reordering to dictionary
        self.dictionary = {ele[0]: ele[1] for ele in test_dict_list}
        return self.dictionary

    def translateVariable(self, name):
        if not self.generalize_vars or name == self.replacementStrategy.getStringReplacer():  # safeguard against replacement of already generalized strings
            return name
        self.dictionary[name] = self._getVariableName()

        return name  # self._getVariableName()

    '''def translateClass(self, name):
        if not self.generalize_classes:
            return name
        self.class_counter = self.class_counter + 1
        self.dictionary[name] = self.class_prefix + str(self.class_counter - 1)
        return name  # self.class_prefix+str(self.class_counter-1)'''

    def isGeneralizationEnabled(self):
        return self.generalize_functions or self.generalize_vars or self.generalize_classes or self.generalize_strings

    def translate(self, name):
        """
        Returns the name in the dictionary that matches to a specific token.
        Basically:
          name: hi
          Dictionary: ["hi":"bye", "hello":"gd bye"]
          return: "bye"
        """
        if name in self.dictionary:
            return self.dictionary[name]
        return name
