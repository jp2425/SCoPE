from service.renameStrategies.replacementStrategy import ReplacementStrategy


class SimpleReplacement(ReplacementStrategy):

    def __init__(self):
        self.variable_prefix = "VAR"
        self.function_prefix = "FUNC"
        self.class_prefix = "CLASS"
        self.string_replacer = "STRING_TOKEN"

        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0

    def getFunctionName(self):
        self.function_counter = self.function_counter + 1
        return self.function_prefix + str(self.function_counter - 1)

    def getVariableName(self):
        self.variable_counter = self.variable_counter + 1
        return self.variable_prefix + str(self.variable_counter - 1)

    def getStringReplacer(self):
        return self.string_replacer