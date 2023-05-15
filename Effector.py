from pyswip import Prolog

def getAllEffectors(prolog):
    effectorList = list(prolog.query("effector(X,Y)"))
    dictEffector = {}
    for i in range(len(effectorList)):
        dictEffector [effectorList[i]["X"]]= effectorList[i]["Y"]

    newdict = {}
    for k,v in dictEffector.items():
        temp = list(prolog.query("effectorValue("+ str(k) +",Y)"))
        if bool(temp):
            newdict[k]= [v, temp[0]["Y"]]
    return newdict


def getEffectorValue(effectorID, prolog):
    query_list = list(prolog.query("effectorValue(" + effectorID +" ,X)"))
    if len(query_list) == 1:
        return str(query_list[0]["X"])
    else: return query_list 


def setEffectorValue(effectorID, value, prolog):
    old_value = str(getEffectorValue(effectorID, prolog))
    list(prolog.query("replace_existing_fact(effectorValue(" + str(effectorID) +" ,"+str(old_value)+"), effectorValue(" + str(effectorID)+ ", "+str(value)+"))"))
    

def resetEffectors(prolog):
    effectors = getAllEffectors(prolog)
    for k, v in effectors.items():
        setEffectorValue(k, "0", prolog)

def checkPreferences(action, prolog):
    #return bool(query("preferencesInstance("+name+", _, _, _)"))
    query_list = list(prolog.query("preferencesInstance("+action+", T, V, E)"))
    if len(query_list)>0:
        for pref in query_list:
            type = pref["T"]
            list(prolog.query("set(" + action + ", " + type + ")."))




