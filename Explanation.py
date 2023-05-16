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
    print (sensors)


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
    print (effectors)
