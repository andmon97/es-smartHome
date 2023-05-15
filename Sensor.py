from pyswip import Prolog
  

import random

def getAllSensor(prolog):
    sensorList = list(prolog.query("sensor(X,Y)"))
    dictsensor = {}
    for i in range(len(sensorList)):
        dictsensor [sensorList[i]["X"]] = sensorList[i]["Y"]
        
    newdict = {}
    for k,v in dictsensor.items():
        temp = list(prolog.query("sensorValue("+str(k)+",Y)"))
        if bool(temp):
            newdict[k]= [v, temp[0]["Y"]]
    return newdict

def getSensorValue(sensorID, prolog):
    query_list = list(prolog.query("sensorValue(" + sensorID +" ,X)"))
    if len(query_list) == 1:
        return str(query_list[0]["X"])
    else: return query_list 

def setSensorValue(sensorID, value, prolog):
    old_value = str(getSensorValue(sensorID, prolog))
    prolog.query("retract(sensorValue(" + str(sensorID) +" ,"+str(old_value)+"), assert(sensorValue(" + str(sensorID)+ ", "+str(value)+")." )
    # query("replace_existing_fact(sensorValue(" + sensorID +" ,_), sensorValue(" + sensorID+ ", "+value+"))")


def generete_random_sensors(prolog):
    sensors = getAllSensor(prolog)
    for k, v in sensors.items():
        if v[0] == 'light':
            setSensorValue(k, random.randint(0,10), prolog)
        elif v[0] == 'temp':
            setSensorValue(k, random.randint(15,20), prolog)
        elif v[0] == 'noise' or v[0] == 'wind':
            setSensorValue(k, random.randint(0,10), prolog)
        elif v[0] == 'rain':
            setSensorValue(k, random.randint(0,1), prolog)
