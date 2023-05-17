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
    print(sensors)
    print(effectors)
    text=""
    text = text + "The action selected is "+ effectors['action'] + ".\n"


    # decode the light setting
    preference = list(prolog.query("preferencesInstance("+effectors['action']+", light, V, E)"))
    if int(sensors['outside_brightness']) >= int(preference[0]['V']):
        text = text + "Since the outside light is greater than the desired light, the expert system has turned off the light and opened the windows.\n"
    else:
        text = text + "Since the outside light is less than the desired light, the expert system has turned on the selected light at the desired value of brightness ("+  str(preference[0]['V']) +" and closed the windows.\n"

    #decode the temperature setting
    preference_temp = list(prolog.query("preferencesInstance("+effectors['action']+", temp, V, E)"))
    
    if int(sensors['inside_temperature']) == int(preference_temp[0]['V']):
         text = text + "Since the inside temperature is equal to the desired temperature the expert system doesn not performs any changes.\n"
    
    
    elif int(sensors['inside_temperature']) < int(preference_temp[0]['V']) and int(sensors['outside_temperature']) > int(preference_temp[0]['V']):
        text = text + "Since the inside temperature is less then the desidered temperature and the outside temperature is greater the desidered one "
        text = text + " the expert system want to open the windows but first check the wind.\n"
        preference_wind = list(prolog.query("preferencesInstance("+effectors['action']+", wind, V, E)"))
        if int(sensors['outside_wind']) <= int(preference_wind[0]['V']):
            text = text + "Since the wind is less or equal to the desidered "
            if int(sensors['outside_rain']) == 0:
                if int(effectors['w1']) == 1 and int(effectors['w2'])== 1:
                    text = text + " and it is not raining, the expert system open w1 and w2."
                else:
                    text = text + " the expert system is not responding.\n"
            else:
                text = text + " but it is raining, the expert system decide to "
                if int(effectors['ac']) != 0:
                    text = text + " turn on the air conditioner (ar) setting the temperature " + str(preference_temp[0]['V']) + ". "
                elif int(effectors['r']) != 0:
                    text = text + " turn on the radiator (r) setting the temperature " + str(preference_temp[0]['V']) + ".\n"
        else: 
            text = text + "Since the wind is greater to the desidered, the expert system decide to "
            if int(effectors['w1']) == 0 and int(effectors['w2']) == 0:
                text = text + "close w1 and w2 and "
                if int(effectors['ac']) != 0:
                    text = text + "turn on the air conditioner (ar) setting the temperature " + str(preference_temp[0]['V']) + ". "
                elif int(effectors['r']) != 0:
                    text = text + "turn on the radiator (r) setting the temperature " + str(preference_temp[0]['V']) + ".\n"
            else: 
                text = text + "the expert system is not responding.\n"
            
    
    elif int(sensors['inside_temperature']) < int(preference_temp[0]['V']) and int(sensors['outside_temperature']) < int(preference_temp[0]['V']):
        text = text + "Since both inside and ouside temperature are less then the desidered temperature, "
        if int(effectors['w1']) == 0 and int(effectors['w2'])==0:
            text = text + " the expert system close w1 and w2 and "
            if int(effectors['ac']) != 0:
                    text = text + "turn on the air conditioner (ar) setting the temperature " + str(preference_temp[0]['V']) + ". "
            elif int(effectors['r']) != 0:
                text = text + "turn on the radiator (r) setting the temperature " + str(preference_temp[0]['V']) + ".\n"
        else: 
            text = text + "the expert system is not responding.\n"


    elif int(sensors['inside_temperature']) > int(preference_temp[0]['V']) and int(sensors['outside_temperature']) > int(preference_temp[0]['V']):
        text = text + "Since both inside and ouside temperature are greater then the desidered temperature, "
        if int(effectors['w1']) == 0 and int(effectors['w2'])==0 :
            text = text + " the expert system close the w1 and w2 and "
            if int(effectors['ac']) != 0:
                    text = text + "turn on the air conditioner (ar) setting the temperature " + str(preference_temp[0]['V']) + ". "
            elif int(effectors['r']) != 0:
                text = text + "turn on the radiator (r) setting the temperature " + str(preference_temp[0]['V']) + ".\n"
        else: 
            text = text + "the expert system is not responding.\n"

    
    elif int(sensors['inside_temperature']) > int(preference_temp[0]['V']) and int(sensors['outside_temperature']) < int(preference_temp[0]['V']):
        text = text + "Since the inside temperature is greater then the desider temperature and the outside temperature is less then the desidered temperature " 
        text = text + " the expert system want to open the windows but first check the wind.\n"
        preference_wind = list(prolog.query("preferencesInstance("+effectors['action']+", wind, V, E)"))
        if int(sensors['outside_wind']) > int(preference_wind[0]['V']):
            text = text + "Since the wind is greater to the desidered, the expert system decide to "
            if int(effectors['w1']) ==0 and int(effectors['w2']) ==0:
                text = text + "close w1 and w2 and "
                if int(effectors['ac']) != 0:
                    text = text + "turn on the air conditioner (ar) setting the temperature " + str(preference_temp[0]['V']) + ". "
                elif int(effectors['r']) != 0:
                    text = text + "turn on the radiator (r) setting the temperature " + str(preference_temp[0]['V']) + ".\n"
            else: 
                text = text + "the expert system is not responding.\n"
        else:
            text = text + "Since the wind is less or equal to the desidered "
            if int(sensors['outside_rain']) == 0:
                if int(effectors['w1']) == 1 and int(effectors['w2']) == 1:
                    text = text + " and it is not raining, the expert system open w1 and w2.\n"
                else:
                    text = text + " the expert system is not responding.\n"
            else:
                text = text + " but it is raining, the expert system decide to "
                if int(effectors['ac']) != 0:
                    text = text + " turn on the air conditioner (ar) setting the temperature " + str(preference_temp[0]['V']) + ".\n"
                elif int(effectors['r']) != 0:
                    text = text + " turn on the radiator (r) setting the temperature " + str(preference_temp[0]['V']) + ".\n"


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
    
