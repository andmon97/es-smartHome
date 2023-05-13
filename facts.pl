%propertyType(TypeId).
propertyType(light).
propertyType(temp).
propertyType(noise).
propertyType(wind).

%sensor(SensorId, TypeId).
:-dynamic(sensor/2).
sensor(brightness_outside, light).
sensor(brightness, light).
sensor(temperature, temp).
sensor(temperature_outside, temp).
sensor(outside_noise, noise).
sensor(outside_wind, wind).


%sensorValue(SensorId, Value).
:-dynamic(sensorValue/2).
sensorValue(brightness, 0).
sensorValue(brightness_outside, 0).
sensorValue(temperature, 10).
sensorValue(temperature_outside, 30).
sensorValue(outside_noise, 20).
sensorValue(outside_wind, 0).


%actuator(ActuatorId, TypeId).
:-dynamic(actuator/2).
actuator(X, noise) :-
    actuator(X, temp).
actuator(l1, light). /* main light */
actuator(l2, light). /* desk light */
actuator(l3, light). /* bedside (left) light */
actuator(l4, light). /* bedside (right) light */
actuator(ac, temp).  /* air conditioner */
actuator(w1, temp). /* window 1 */
actuator(w1, wind).
actuator(rs1, light). /* roller shutter 1*/
actuator(w2, temp). /* window 2 */
actuator(w2, wind).
actuator(rs2, light). /* roller shutter 2*/
actuator(r, temp). /* radiator */



%inside(Id).
:-dynamic(inside/1).
inside(brightness).
inside(temperature).
inside(l1).
inside(l2).
inside(l3).
inside(l4).
inside(ac).
inside(r).


%actuatorValue(ActuatorId, Value).
:-dynamic(actuatorValue/2).
actuatorValue(l1, 0). /* main light */
actuatorValue(l2, 0). /* desk light */
actuatorValue(l3, 0). /* bedside (left) light */
actuatorValue(l4, 0). /* bedside (right) light */
actuatorValue(w1, 0).  /* window 1 */
actuatorValue(w2, 0).  /* window 2 */
actuatorValue(rs1, 0). /* roller shutter 1*/
actuatorValue(rs2, 0). /* roller shutter 2*/
actuatorValue(r, 0). /* radiator */
actuatorValue(ac, 0). /* air conditioner */


%preferencesInstance(PiiD, TypeId, ExpectedValueSensor, Actuators).
:-dynamic(preferencesInstance/4).
preferencesInstance(nullPreference, _, 0, []).
preferencesInstance(study, light, 10, [l2, rs1]). /* if study only desk light */
preferencesInstance(study, temp, 20, [ac, r, w1, w2]).
preferencesInstance(study, wind, 0, [w1,w2]). /* close windows for wind*/
preferencesInstance(study, noise, 0, [ac, w1, w2]).

preferencesInstance(sleep, light, 0, [l1, l2, l3, l4, rs1, rs2]). /* turn off all lights and roller shutters */
preferencesInstance(sleep, temp, 25, [ac, r, w1, w2]).
preferencesInstance(sleep, wind, 0, [w1,w2]). /* close windows for wind*/
preferencesInstance(sleep, noise, 2, [ac, w1, w2]).

preferencesInstance(turn_off, TypeId, 0, Actuators) :- setof(X, actuator(X,TypeId),Actuators).
preferencesInstance(turn_on, TypeId, 10, Actuators) :- setof(X, actuator(X,TypeId),Actuators).

preferencesInstance(movie, light, 5, [l3,l4, rs1, rs2]). /* if movie only bedside lights */
preferencesInstance(movie, temp, 25, [r, w1, w2, ac]).
preferencesInstance(movie, wind, 0, [w1,w2]). /* close windows for wind*/
preferencesInstance(movie, noise, 5, [ac, w1, w2]).

preferencesInstance(clean, light, 10, [l1, rs1, rs2]). /* if clean only roller s*/
preferencesInstance(clean, temp, 20, [r, ac, w1,w2]). /* open windows */
preferencesInstance(clean, wind, 5, [w1,w2]). /* open windows for wind*/