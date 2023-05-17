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
    if int(sensors['outside_temperature']) == int(preference[0]['V']):
         text = text + "Since the inside temperature is equal to the desired temperature (" + sensors['outside_temperature'] + ' == ' + preference[0]['V'] + "), the expert system doesn not performs any changes.\n"
    elif int(sensors['inside_temperature']) < int(preference[0]['V']) and int(sensors['outside_temperature']) > int(preference[0]['V']):
        text = text  

    # decode the light setting
    preference = list(prolog.query("preferencesInstance("+effectors['action']+", light, V, E)"))
    if int(sensors['outside_brightness']) >= int(preference[0]['V']):
        text = text + "Since the outside light is greater than the desired light, the expert system has turned off the light and opened the windows.\n"
    else:
        text = text + "Since the outside light is less than the desired light, the expert system has turned on the selected light at the desired value of brightness ("+  str(preference[0]['V']) +" and closed the windows.\n"

    
    # decode the noise setting
    preference = list(prolog.query("preferencesInstance("+effectors['action']+", noise, V, E)"))
    preferenceTemp = list(prolog.query("preferencesInstance("+effectors['action']+", temp, V, E)"))
    if int(sensors['outside_noise']) > preference[0]['V']:
        text = text + "Since the outside noise is greater than the desired noise, the expert system "
        if int(sensors['outside_temperature']) == int(preferenceTemp[0]['V']):
            text = text + "has closed the windows.\n"
        else:
            if int(sensors['outside_temperature']) < int(preferenceTemp[0]['V']):
                text = text + "has closed the windowsd and has turned on the air conditioning because the temperature outside is greater than the temperature inside.\n"
            else:
                text = text + "has closed the windows and has turned on the radiator because the temperature outside is less than the temperature inside.\n"
    else:
        text = text + "Since the outside noise is less than the desired noise, the expert system has opened the windows.\n"
    return text
    
