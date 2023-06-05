from pyswip import Prolog
import datetime 

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
    list(prolog.query("replace_existing_fact(sensorValue(" + str(sensorID) +" ,"+str(old_value)+"), sensorValue(" + str(sensorID)+ ", "+str(value)+"))." ))
    

def generete_random_sensors(prolog):
    sensors = getAllSensor(prolog)
    #import the date
    date = datetime.datetime.now()
    f = open("logActions.txt", "w")

    for k, v in sensors.items():
        if v[0] == 'light':
            if k=='outside_brightness':
               n = random.randint(0,10)
               setSensorValue(k, n, prolog)
            else:
                n = 0
                setSensorValue(k, n, prolog)
        elif v[0] == 'temp':
            # if is winter
            if date.month in [12,1,2,3]:
                n = random.randint(0,10)
                setSensorValue(k, n, prolog)
            # if is spring
            elif date.month in [4,5,6]:
                n = random.randint(10,20)
                setSensorValue(k, n, prolog)
            # if is summer
            elif date.month in [7,8,9]:
                n = random.randint(20,30)
                setSensorValue(k, n, prolog)
            # if is autumn
            elif date.month in [10,11]:
                n = random.randint(10,20)
                setSensorValue(k, n, prolog)
        elif v[0] == 'noise' or v[0] == 'wind':
            n = random.randint(0,10)
            setSensorValue(k, n, prolog)
        elif v[0] == 'rain':
            n = random.randint(0,1)
            setSensorValue(k, n, prolog)
        
        # print in the logActionas file the string setSensorValue(k, n)
        f.write("setSensorValue("+k+", "+str(n)+")\n")
    f.close()


