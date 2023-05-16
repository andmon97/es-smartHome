%propertyType(TypeId).
propertyType(light).
propertyType(temp).
propertyType(noise).
propertyType(wind).
propertyType(rain).

%sensor(SensorId, TypeId).
:-dynamic(sensor/2).
sensor(outside_brightness, light).
sensor(inside_brightness, light).
sensor(inside_temperature, temp).
sensor(outside_temperature, temp).
sensor(outside_noise, noise).
sensor(outside_wind, wind).
sensor(outside_rain, rain).



%sensorValue(SensorId, Value).
:-dynamic(sensorValue/2).
sensorValue(inside_brightness, 0).
sensorValue(outside_brightness, 10).
sensorValue(outside_temperature, 10).
sensorValue(inside_temperature, 30).
sensorValue(outside_noise, 3).
sensorValue(outside_wind, 0).
sensorValue(outside_rain, 1).


%effector(EffectorId, TypeId).
:-dynamic(effector/2).
effector(X, noise) :-
    effector(X, temp).
effector(l1, light). /* main light */
effector(l2, light). /* desk light */
effector(l3, light). /* bedside (left) light */
effector(l4, light). /* bedside (right) light */
effector(rs1, light). /* roller shutter 1*/
effector(rs2, light). /* roller shutter 2*/
effector(ac, temp).  /* air conditioner */
effector(r, temp). /* radiator */
effector(w1, temp). /* window 1 */
effector(w2, temp). /* window 2 */
effector(w1, wind).
effector(w2, wind).
effector(w1, rain).
effector(w2, rain).



%inside(Id).
:-dynamic(inside/1).
inside(inside_brightness).
inside(inside_temperature).
inside(l1).
inside(l2).
inside(l3).
inside(l4).
inside(ac).
inside(r).


%effectorValue(EffectorId, Value).
:-dynamic(effectorValue/2).
effectorValue(l1, 0). /* main light */
effectorValue(l2, 0). /* desk light */
effectorValue(l3, 0). /* bedside (left) light */
effectorValue(l4, 0). /* bedside (right) light */
effectorValue(w1, 0).  /* window 1 */
effectorValue(w2, 0).  /* window 2 */
effectorValue(rs1, 0). /* roller shutter 1*/
effectorValue(rs2, 0). /* roller shutter 2*/
effectorValue(r, 0). /* radiator */
effectorValue(ac, 0). /* air conditioner */


%preferencesInstance(PiiD, TypeId, ExpectedValueSensor, Effectors).
:-dynamic(preferencesInstance/4).
preferencesInstance(nullPreference, _, 0, []).
preferencesInstance(study, light, 10, [l2, rs1]). /* if study only desk light */
preferencesInstance(study, temp, 20, [ac, r, w1, w2]).
preferencesInstance(study, wind, 3, [w1,w2]). /* close windows for wind*/
preferencesInstance(study, noise, 0, [ac, w1, w2]).

preferencesInstance(sleep, light, 0, [l1, l2, l3, l4, rs1, rs2]). /* turn off all lights and roller shutters */
preferencesInstance(sleep, temp, 25, [ac, r, w1, w2]).
preferencesInstance(sleep, wind, 0, [w1,w2]). /* close windows for wind*/
preferencesInstance(sleep, noise, 0, [ac, w1, w2]).

preferencesInstance(turn_off, TypeId, 0, Effectors) :- setof(X, effector(X,TypeId),Effectors).
preferencesInstance(turn_on, TypeId, 10, Effectors) :- setof(X, effector(X,TypeId),Effectors).

preferencesInstance(movie, light, 5, [l3,l4, rs1, rs2]). /* if movie only bedside lights */
preferencesInstance(movie, temp, 25, [r, w1, w2, ac]).
preferencesInstance(movie, wind, 3, [w1,w2]). /* close windows for wind*/
preferencesInstance(movie, noise, 0, [ac, w1, w2]).

preferencesInstance(clean, light, 10, [l1, rs1, rs2]). /* if clean only roller s*/
preferencesInstance(clean, temp, 20, [r, ac, w1,w2]). /* open windows */
preferencesInstance(clean, wind, 5, [w1,w2]). /* open windows for wind*/

preferencesInstance(music, light, 5, [l1, l2, l3, l4, rs1, rs2]). /* if study only desk light */
preferencesInstance(music, temp, 20, [ac, r, w1, w2]).
preferencesInstance(music, wind, 0, [w1,w2]). /* close windows for wind*/
preferencesInstance(music, noise, 0, [ac, w1, w2]).