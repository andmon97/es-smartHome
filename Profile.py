def getProfile(prolog):
    actions=['study', 'movie', 'sleep', 'clean', 'music']
    type = ['light', 'temp', 'wind', 'noise' ]

    text=""
    for act in actions:
        if act=="movie":
             action="watching a movie "
        elif act=="music":
            action="listening music"
        else: 
            action= act +"ing"
        text = text + "While the user is " + action + ", he/she want: \n"
        for t in type:
            preference = list(prolog.query("preference(" + act + ", " + t + ", V, E)"))
            text = text + t + " " + str(preference[0]['V']) + "\n"
        text = text +"\n\n"
    return text

def updateFacts(prolog, new_profile):
    if new_profile["light"] != "":
        old_preference_light = list(prolog.query("preference(" + new_profile['action']+", light, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", light," + str(old_preference_light[0]['V']) + ", " + str(old_preference_light[0]['E']) +"), preference(" + new_profile['action']+ ", light, " + new_profile['light']+ "," + str(old_preference_light[0]['E']) +"))"))
    
    if new_profile["temp"] != "":
        old_preference_temp = list(prolog.query("preference(" + new_profile['action']+", temp, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", temp," + str(old_preference_temp[0]['V']) + ", " + str(old_preference_temp[0]['E']) +"), preference(" + new_profile['action']+ ", temp, " + new_profile['temp']+ "," + str(old_preference_temp[0]['E']) +"))"))
    
    if new_profile["wind"] != "":
        old_preference_wind = list(prolog.query("preference(" + new_profile['action']+", wind, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", wind," + str(old_preference_wind[0]['V']) + ", " + str(old_preference_wind[0]['E']) +"), preference(" + new_profile['action']+ ", wind, " + new_profile['temp']+ "," + str(old_preference_wind[0]['E']) +"))"))
    
    if new_profile["noise"] != "":
        old_preference_noise = list(prolog.query("preference(" + new_profile['action']+", noise, V, E)."))
        list(prolog.query("replace_existing_fact(preference(" + new_profile['action']+ ", noise," + str(old_preference_noise[0]['V']) + ", " + str(old_preference_noise[0]['E']) +"), preference(" + new_profile['action']+ ", noise, " + new_profile['noise']+ "," + str(old_preference_noise[0]['E']) +"))"))
    