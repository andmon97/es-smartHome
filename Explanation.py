sensors = {}
effectors = {}

def getSensorValues():
    f = open("logActions.txt", "r")
    lines = f.readlines()
    f.close()
    for l in lines:
        if 'setSensorValue' in l:
            nameSensor = l.split('(')[1].split(',')[0]
            valueSensor = l.split(',')[1].split(')')[0]
            sensors[nameSensor] = valueSensor


def getEffectorsValue():
    f = open("logActions.txt", "r")
    # read all the lines in a reversed orders
    lines = f.readlines()[::-1]
    f.close()
    # read all the lines that start with set() and stop when you find the first line that starts with setSensorValue
    for l in lines:
        if 'setEffector(' in l:
            # save the name of the effector and the value
            nameEffector = l.split('(')[1].split(',')[0]
            valueEffector = l.split(',')[1].split(')')[0]
            effectors[nameEffector] = valueEffector
        elif 'set(' in l:
            effectors['action'] = l.split('(')[1].split(',')[0]

def getExplanation(prolog):
    text=""
    text = text + "The action selected is "+ effectors['action'] + ".\n"
    preference = list(prolog.query("preferencesInstance("+effectors['action']+", temp, V, E)"))
    print(preference[0]['V'])
    if sensors['outside_temperature'] == preference[0]['V']:
         text = text + "Since the inside temperature is equal to the desired temperature (" + sensors['outside_temperature'] + ' == ' + preference[0]['V'] + "), the expert system doesn not performs any changes.\n"
    elif sensors['inside_temperature'] < preference[0]['V'] and sensors['outside_temperature'] > preference[0]['V']:
        text = text  
   
    return text
    
