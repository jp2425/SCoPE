
from service.TokenProcessorService import TokenProcessorService
from service.codePostProcessService import CodePostProcessService
from service.renameStrategies.minifyReplacement import MinifyReplacement
from service.renameStrategies.simpleReplacement import SimpleReplacement
from store.tokenStore import TokenStore
from service.generalizeService import GeneralizeService
import time

class ProcessCodeController:

    def __int__(self):
        pass

    def processCode(self, requestJson):
        generalize_functions = requestJson['generalizeFunctionNames']
        generalize_variables = requestJson['generalizeVariableNames']
        generalize_strings = requestJson['generalizeStrings']
        tryRecoverFromErrors = requestJson['tryRecoverFromErrors']
        returnType = requestJson['returnType']
        replacementStrategy = None
        if int(requestJson['replacementStrategy'] == 1):
            replacementStrategy = MinifyReplacement()
        else:
            #default
            replacementStrategy = SimpleReplacement()

        start = time.time()
        store = TokenStore()
        generalizer = GeneralizeService(replacementStrategy,generalize_functions, generalize_variables, generalize_strings)
        t = TokenProcessorService(store, generalizer)
        out = t.process(requestJson['code'], try_recover_from_errors=tryRecoverFromErrors)
        if int(returnType) == 1:
            servicePostProcess = CodePostProcessService(generalizer)
            return servicePostProcess.process(requestJson['code'])
        end = time.time()
        print()
        print("[*] Estatísticas:")
        print("Tempo de execução: ", end-start)
        print("Tokens processados: ", len(out))
        print("\n\n")
        return out

