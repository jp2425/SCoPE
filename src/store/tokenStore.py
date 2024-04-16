from service.generalizeService import GeneralizeService


class TokenStore:

    def __init__(self):
        self.tokens = []

    def addToken(self, token):
        self.tokens.append(token)

    def addTokens(self, tokens):
        self.tokens = self.tokens + tokens

    def getTranslatedTokens(self, generalize: GeneralizeService):
        for i in range(len(self.tokens)):
            self.tokens[i] = generalize.translate(self.tokens[i])
        return self.tokens
