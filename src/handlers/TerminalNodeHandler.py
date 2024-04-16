class TerminalNodeHandler:

    def __init__(self,generalizer):
        self.generalizer = generalizer

    def handle(self, name):
        if not isinstance(name, str):
            name = name.getText()
        return self.generalizer.translateLiteral(name)