import re
import traceback

from service.generalizeService import GeneralizeService


class CodePostProcessService:

    def __init__(self,generalizer:GeneralizeService, remove_comments = True, normalize_spacing = True, remove_newlines = True ):
        self.general_regex = r'(?<![a-zA-Z0-9_]){0}(?![a-zA-Z0-9_]|@TOKEN@)' #regex that covers all situations. the @TOKEN@ is used to avoid replace a string that was already replaced.
        #self.regex_replace_vars = r"(?<=[ \!\[\*\&,\(\+\-\=]){0}(?=[. ;,\[\]\))\<\>\=\+\-}])" #all tokens that have space, "*" or "&" before and space, ".", ";", "=", ")" ,"}" after, not including (https://www.rexegg.com/regex-disambiguation.html#lookarounds)
        self.regex_replace_vars = self.general_regex
        self.regex_comments =  r'\/\/[^\n]*|\/\*[\s\S]*?\*\/|//.*?\n|/\*.*?\*/'
        self.regex_function = r"(?<=[ *]){0}(?=[( ]+(\( )?)|^{0}(?=[( ]+(\( )?)"
        self.regex_function = self.general_regex
        self.regex_string = r'[\"\'](.*?)[\"\']'

        self.generalizer = generalizer
        self.remove_comments = remove_comments
        self.normalize_spacing = normalize_spacing
        self.remove_newlines = remove_newlines
    def process(self, code,):
        if self.remove_comments:
            code = self.removeComments(code)
        if self.normalize_spacing:
            code = self.normalizeSpacing(code)
        if self.remove_newlines:
            code = self.removeNewlines(code)
        if self.generalizer.generalize_strings:
            code = self.replaceStrings(code)
        if self.generalizer.generalize_vars or self.generalizer.generalize_functions:
            if self.generalizer.dictionary is None:
                raise Exception("The tokens dict cannot be null")
            code = self.replaceVarsCode(self.generalizer.dictionary, self.replaceFunctionsCode(self.generalizer.dictionary, code))
        return code.replace("@TOKEN@","") # lets remove the special "token" added to prevent replacement of already replaced tokens
    def replaceStrings(self,code):
        """
        Replace strings with the token to replace + special value to prevent replace in future steps the new token with other, what may cause problems.
        """
        return re.sub(self.regex_string, self.generalizer.replacementStrategy.getStringReplacer()+"@TOKEN@", code)
    def removeComments(self,code):
        return re.sub(self.regex_comments, '\n', code)

    def normalizeSpacing(self,code):
        return " ".join(code.split()).replace("\t", " ")

    def removeNewlines(self,code):
        return code.replace("\n", "")
    def replaceVarsCode(self, tokensDictionary: dict, code: str):
        """
        Replace variable with the token to replace + special value to prevent replace in future steps the new token with other, what may cause problems.
        """
        for token in self.generalizer.sortDict():
            reg = self.regex_replace_vars.replace("{0}", re.escape(token))
            code = re.sub(reg, tokensDictionary[token]+"@TOKEN@", code)
        return code

    def replaceFunctionsCode(self,tokensDictionary: dict, code: str):
        """
        Replace function name with the token to replace + special value to prevent replace in future steps the new token with other, what may cause problems.
        """

        for token in tokensDictionary:
            reg = self.regex_function.replace("{0}", re.escape(token))
            code = re.sub(reg, tokensDictionary[token]+"@TOKEN@", code)
        return code
