replace_existing_fact(OldFact, NewFact) :-
    call(OldFact), 
    !,
    retract(OldFact),
    assertz(NewFact).


remove_existing_fact(OldFact) :-
    call(OldFact), 
    retract(OldFact).


%outside(Id).
outside(Id) :- 
	\+ inside(Id).


%setInsideEffectors(Effectors, Value).
setInsideEffectors([H|T], Y) :-
    extractInsideEffectors([H|T], [], L),
    setEffectors(L, Y).

%setOutsideEffectors(Effectors, Value).
setOutsideEffectors([H|T], Y) :-
    extractOutsideEffectors([H|T], [], L),
    setEffectors(L, Y).

%setEffectors(Effectors, Value).
setEffectors([H|T], Y) :-
    T \== [],
    !,
    setEffectors(T, Y),
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)).

setEffectors([H|_], Y) :-
    !,
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)).

setEffectors(_, _).

%setEffectors(Effectors, Value).
setEffectors([H|T], Y) :-
    T \== [],
    !,
    setEffectors(T, Y),
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)).

setEffectors([H|_], Y) :-
    !,
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)).

setEffectors(_, _).
    

%extractInsideEffectors(List, NewList, variable).
extractInsideEffectors([H|T], L,X) :-
    T \== [],
    inside(H),
    !,
    extractInsideEffectors(T, [H|L], X).

extractInsideEffectors([H|T], L, X) :-
    T\== [],
    \+ inside(H),
    !,
    extractInsideEffectors(T, L, X).

extractInsideEffectors([H|_], L,X) :-
    \+ inside(H),
    !,
    X = L.

extractInsideEffectors([H|_], L, X) :-
    inside(H),
    !,
    X = [H|L].

extractInsideEffectors(_, L, X) :-
    X = L.
 

%extractOutsideEffectors(List, NewList, variable).
extractOutsideEffectors([H|T], L,X) :-
    T \== [],
    outside(H),
    !,
    extractOutsideEffectors(T, [H|L], X).

extractOutsideEffectors([H|T], L, X) :-
    T\== [],
    \+ outside(H),
    !,
    extractOutsideEffectors(T, L, X).

extractOutsideEffectors([H|_], L,X) :-
    \+ outside(H),
    !,
    X = L.

extractOutsideEffectors([H|_], L, X) :-
    outside(H),
    !,
    X = [H|L].

extractOutsideEffectors(_, L, X) :-
    X = L.

%set(PIId).
set(PIId) :-  set(PIId, _).

%set(PIId, TypeId).
set(PIId, light) :- 
    sensor(SensorId_outside, light),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X),
    preferencesInstance(PIId, light, Y, Effectors),
    X >= Y,
	setOutsideEffectors(Effectors, Y),
	setInsideEffectors(Effectors, 0).
    
set(PIId, light) :- 
    sensor(SensorId_outside, light),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X),
    preferencesInstance(PIId, light, Y, Effectors),
    X < Y,
	setOutsideEffectors(Effectors, 0), 
	setInsideEffectors(Effectors, Y).

setInsideEffectors_temp(temp_inside, temp_pref) :-
    temp_inside < temp_pref,
    setEffectors(r, temp_pref).

setInsideEffectors_temp(temp_inside, temp_pref) :-
    temp_inside > temp_pref,
    setEffectors(ac, temp_pref).

check_rain(Y_temp) -:
    sensor(SensorId_outside, rain),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_rain),
    X_rain == 0,
	setOutsideEffectors(Effectors, 1),
	setInsideEffectors(Effectors, 0).

check_rain(Y_temp) -:
    sensor(SensorId_outside, rain),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_rain),
    X_rain == 1,
	setOutsideEffectors(Effectors, 0),
	setInsideEffectors_temp(Effectors, Y_temp).


set(PIId, temp) :-
    preferencesInstance(PIId, temp, Y_temp, Effectors),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_outside),
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_inside),
    X_inside < Y_temp,
    X_outside > Y_temp,
    %check the value of the sensor wind 
    sensor(SensorId_outside, wind),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_wind),
    preferencesInstance(PIId, wind, Y_wind, Effectors),
    X_wind <= Y_wind,
    check_rain(Y_temp).


set(PIId, temp) :-
    preferencesInstance(PIId, temp, Y_temp, Effectors),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_outside),
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_inside),
    X_inside < Y_temp,
    X_outside > Y_temp,
    %check the value of the sensor wind 
    sensor(SensorId_outside, wind),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_wind),
    preferencesInstance(PIId, wind, Y_wind, Effectors),
    X_wind > Y_wind,
	setOutsideEffectors(Effectors, 0),
	setInsideEffectors_temp(X_inside, Y_temp).

set(PIId, temp) :-
    preferencesInstance(PIId, temp, Y, Effectors),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_outside),
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_inside),
    X_inside < Y,
    X_outside < Y,
	setOutsideEffectors(Effectors, 0),
	setInsideEffectors_temp(X_inside, Y).


set(PIId, temp) :-
    preferencesInstance(PIId, temp, Y, Effectors),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_outside),
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_inside),
    X_inside > Y,
    X_outside > Y,
	setOutsideEffectors(Effectors, 0),
	setInsideEffectors_temp(X_inside, Y).

set(PIId, temp) :-
    preferencesInstance(PIId, temp, Y, Effectors),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_outside),
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_inside),
    X_inside > Y,
    X_outside < Y,
    %check the value of the sensor wind 
    sensor(SensorId_outside, wind),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_wind),
    preferencesInstance(PIId, wind, Y_wind, Effectors),
    X_wind <= Y_wind,
	check_rain(Y_temp).


set(PIId, temp) :-
    preferencesInstance(PIId, temp, Y, Effectors),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_outside),
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_inside),
    X_inside > Y,
    X_outside < Y,
    %check the value of the sensor wind 
    sensor(SensorId_outside, wind),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_wind),
    preferencesInstance(PIId, wind, Y_wind, Effectors),
    X_wind > Y_wind,
	setOutsideEffectors(Effectors, 0),
	setInsideEffectors_temp(X_inside, Y).


set(PIId, noise) :-
    preferencesInstance(PIId, noise, Y_noise, Effectors),
    sensor(SensorId_outside, noise),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_noise_outside),
    X_noise_outside > Y_noise,
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_temp_inside),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_temp_outside),
    preferencesInstance(PIId, temp, Y_temp, Effectors),
    X_temp_inside \== Y_temp,
    setOutsideEffectors(Effectors, 0),
    setEffectors(ac, Y_temp).

set(PIId, noise) :-
    preferencesInstance(PIId, noise, Y_noise, Effectors),
    sensor(SensorId_outside, noise),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_noise_outside),
    X_noise_outside > Y_noise,
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_temp_inside),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_temp_outside),
    preferencesInstance(PIId, temp, Y_temp, Effectors),
    X_temp_inside == Y_temp,
    setOutsideEffectors(Effectors, 0).

set(PIId, noise) :-
    preferencesInstance(PIId, noise, Y_noise, Effectors),
    sensor(SensorId_outside, noise),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_noise_outside),
    X_noise_outside > Y_noise,
    sensor(SensorId_inside, temp),
    inside(SensorId_inside),
    sensorValue(SensorId_inside, X_temp_inside),
    sensor(SensorId_outside, temp),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X_temp_outside),
    preferencesInstance(PIId, temp, Y_temp, Effectors),
    X_temp_inside \== Y_temp,
    setOutsideEffectors(Effectors, 0).
    setInsideEffectors_temp(X_temp_inside, Y_temp)

%memberCheck(Element, List).
memberCheck(H,[H|_]).
memberCheck(H,[_|T]) :- memberCheck(H,T).