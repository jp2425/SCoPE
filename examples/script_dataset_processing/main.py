import json as simplejson
import pandas as pd
import json
import multiprocessing
import time
import sys
sys.path.append('../../src')

from service.TokenProcessorService import TokenProcessorService
from service.codePostProcessService import CodePostProcessService
from service.generalizeService import GeneralizeService
from service.renameStrategies.minifyReplacement import MinifyReplacement
from store.tokenStore import TokenStore


print("[*] Loading dataset... ")
pd.io.json._json.loads = lambda s, *a, **kw: json.loads(s)
pd.io.json._json.loads = lambda s, *a, **kw: simplejson.loads(s)
pd.io.json._json.loads = lambda s, *a, **kw: pd.json_normalize(simplejson.loads(s))

df = pd.read_json("dataset.json", lines=True) # <<<<------------------------- Change here the location of the dataset (JSON)!
print(df)
#df = df.iloc[:100] # DATASET Subset (TESTING)
cores = multiprocessing.cpu_count()

print(f"[*] Starting processing with {cores} threads")
from pandarallel import pandarallel as pd
pd.initialize(progress_bar=True,nb_workers=cores)


def processCodeNoRecoveryErrors(code):
    generalize_functions = True
    generalize_variables = True
    generalize_strings = False
    tryRecoverFromErrors = False
    returnType = 1
    replacementStrategy = MinifyReplacement()

    start = time.time()
    store = TokenStore()
    generalizer = GeneralizeService(replacementStrategy, generalize_functions, generalize_variables, generalize_strings)
    t = TokenProcessorService(store, generalizer)
    out = t.process(code, try_recover_from_errors=tryRecoverFromErrors)
    if out is None:
        return out
    if int(returnType) == 1:
        servicePostProcess = CodePostProcessService(generalizer)
        pr = servicePostProcess.process(code)
        return pr
    end = time.time()
    print()
    print("[*] Estatísticas:")
    print("Tempo de execução: ", end - start)
    print("Tokens processados: ", len(out))
    print("\n\n")
    return out


def processCodeRecoveryErrors(code):
    generalize_functions = True
    generalize_variables = True
    generalize_strings = False
    tryRecoverFromErrors = True
    returnType = 1
    replacementStrategy = MinifyReplacement()

    start = time.time()
    store = TokenStore()
    generalizer = GeneralizeService(replacementStrategy, generalize_functions, generalize_variables, generalize_strings)
    t = TokenProcessorService(store, generalizer)
    out = t.process(code, try_recover_from_errors=tryRecoverFromErrors)
    if int(returnType) == 1:
        servicePostProcess = CodePostProcessService(generalizer)
        pr = servicePostProcess.process(code)
        return pr
    end = time.time()
    print()
    print("[*] Stats:")
    print("Execution time: ", end - start)
    print("Number of processed tokens: ", len(out))
    print("\n\n")
    return out


def processCode(code):
    out = processCodeNoRecoveryErrors(code)
    if out is None:
        return [1, processCodeRecoveryErrors(code)]
    return [0, out]


start = time.time()

# Create a new column, 'func_ch', with the changed values
df['func_ch'] = df['func'].parallel_apply(processCode)

print("[*] Processed ended. Splitting the column in two (func_ch e func_ch_err)")
df['func_ch_err'] = df['func_ch'].apply(lambda x: x[1] if x[0] == 1 else None) #the functions that had errors during processing will be placed in this column
df['func_ch'] = df['func_ch'].apply(lambda x: x[1] if x[0] == 0 else None) #the others will be placed here

end = time.time()
print("[*] Final dataframe")
print(df)
print("[*] Execution time: ", end - start)

print("[*] Saving the final dataframe (out.json)")
df.to_json("out.json", orient="records")