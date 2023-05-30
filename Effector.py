from pyswip import Prolog
import random

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
    
def generete_random_effectors(prolog):
    sensors = getAllEffectors(prolog)
    for k, v in sensors.items():
        if v[0] == 'light':
            setEffectorValue(k, random.randint(0,10), prolog)
        elif v[0] == 'temp':
            setEffectorValue(k, random.randint(1,50), prolog)


def resetEffectors(prolog):
    effectors = getAllEffectors(prolog)
    for k, v in effectors.items():
        setEffectorValue(k, "0", prolog)

def checkPreferences(action, prolog):
    #return bool(query("preference("+name+", _, _, _)"))
    # open the logActions file in append
    f = open("logActions.txt", "a")
    query_list = list(prolog.query("preference("+action+", T, V, E)"))
    i=0
    if len(query_list)>0:
        for pref in query_list:
            type = pref["T"]
            f.write("set(" + action + ", " + type + ").\n")
            list(prolog.query("set(" + action + ", " + type + ")."))
            
    f.close()




