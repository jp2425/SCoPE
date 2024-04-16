from service.renameStrategies.replacementStrategy import ReplacementStrategy


class MinifyReplacement(ReplacementStrategy):

    def __init__(self):
        self.current_translation = 'a'
        self.string_replacer = "S"

    def _translate(self):
        """
        function we use to get the current value to translate
        """
        result = self.current_translation
        self._increment_translation()
        return result

    def _increment_translation(self):
        """
        function that changes the next translated value
        """
        chars = list(self.current_translation)
        index = len(chars) - 1

        while index >= 0:
            if chars[index] < 'z':
                chars[index] = chr(ord(chars[index]) + 1)
                break
            else:
                chars[index] = 'a'
                index -= 1

        if index < 0:
            chars = ['a'] + chars

        self.current_translation = ''.join(chars)


    def getFunctionName(self):
        """
        The translation of function / variable names is the same
        """
        return self._translate()

    def getVariableName(self):
        """
        The translation of function / variable names is the same
        """
        return self._translate()

    def getStringReplacer(self):
        return self.string_replacer