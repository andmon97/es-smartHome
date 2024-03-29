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
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)),
    % write in a file the line of code to set the effector H to the value Y
    open('logActions.txt', append, Stream),
    write(Stream, 'setEffector('), write(Stream, H), write(Stream, ','), write(Stream, Y), write(Stream, ').'),nl(Stream),
    close(Stream).


setEffectors([H|_], Y) :-
    !,
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)),
    % write in a file the line of code to set the effector H to the value Y
    open('logActions.txt', append, Stream),
    write(Stream, 'setEffector('), write(Stream, H), write(Stream, ','), write(Stream, Y), write(Stream, ').'),nl(Stream),
    close(Stream).

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

%set(IdAction).
set(IdAction) :-  set(IdAction, _).

%set(IdAction, IdCondition).
set(IdAction, light) :- 
    sensor(SensorId_outside, light),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X),
    preference(IdAction, light, Y, Effectors),
    X >= Y,
	setOutsideEffectors(Effectors, Y),
	setInsideEffectors(Effectors, 0).
    
set(IdAction, light) :- 
    sensor(SensorId_outside, light),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X),
    preference(IdAction, light, Y, Effectors),
    X < Y,
	setOutsideEffectors(Effectors, 0), 
	setInsideEffectors(Effectors, Y).

setInsideEffectors_temp(X_temp_inside, Y_temp) :-
    (X_temp_inside < Y_temp ->  setEffectors([r], Y_temp), setEffectors([ac], 0); setEffectors([ac], Y_temp), setEffectors([r], 0) ).





set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_insideTemp, temp),
    sensorValue(SensorId_insideTemp, X_inside),
    inside(SensorId_insideTemp),
    X_inside =:= Y_temp,
    !.


set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside < Y_temp,
    X_outside > Y_temp,
	%check the value of the sensor wind 
    sensor(SensorId_wind, wind),
    outside(SensorId_wind),
    sensorValue(SensorId_wind, X_wind),
    preference(IdAction, wind, Y_wind, EffectorsWind),
    (X_wind =< Y_wind,
    sensor(SensorId_rain, rain),
    sensorValue(SensorId_rain, X_rain),
        (X_rain =:= 0 ->
        setOutsideEffectors(EffectorsTemp, 1),
        setInsideEffectors(EffectorsTemp, 0)
        ;
        setOutsideEffectors(EffectorsTemp, 0),
        setInsideEffectors_temp(X_inside, Y_temp)
        )
    ; 
    setOutsideEffectors(EffectorsTemp, 0),
	setInsideEffectors_temp(X_inside, Y_temp)
    ).







set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside < Y_temp,
    X_outside < Y_temp,
	setOutsideEffectors(EffectorsTemp, 0),
	setInsideEffectors_temp(X_inside, Y_temp).


set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside > Y_temp,
    X_outside > Y_temp,
	setOutsideEffectors(EffectorsTemp, 0),
	setInsideEffectors_temp(X_inside, Y_temp).



    
set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside > Y_temp,
    X_outside < Y_temp,
    %check the value of the sensor wind 
    sensor(SensorId_wind, wind),
    sensorValue(SensorId_wind, X_wind),
    preference(IdAction, wind, Y_wind, EffectorsWind),
    (X_wind > Y_wind -> 
    setOutsideEffectors(EffectorsTemp, 0), 
    setOutsideEffectors(EffectorsWind, 0), 
    setInsideEffectors_temp(X_inside, Y_temp)
    ; 
    sensor(SensorId_rain, rain),
    sensorValue(SensorId_rain, X_rain),
        (X_rain =:= 0 ->
        setOutsideEffectors(EffectorsTemp, 1),
        setOutsideEffectors(EffectorsWind, 1),
        setInsideEffectors(EffectorsTemp, 0)
        ;
        setOutsideEffectors(EffectorsTemp, 0),
        setOutsideEffectors(EffectorsWind, 0),
        setInsideEffectors_temp(X_inside, Y_temp)
        )
    ). 


set(IdAction, noise) :-
    preference(IdAction, noise, Y_noise, EffectorsNoise),
    sensor(SensorId_noise, noise),
    sensorValue(SensorId_noise, X_noise_outside),
    X_noise_outside > Y_noise,
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_temp_inside),
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    X_temp_inside \== Y_temp,
    setOutsideEffectors(EffectorsNoise, 0),
    setInsideEffectors_temp(X_temp_inside, Y_temp).

set(IdAction, noise) :-
    preference(IdAction, noise, Y_noise, EffectorsNoise),
    sensor(SensorId_noise, noise),
    sensorValue(SensorId_noise, X_noise_outside),
    X_noise_outside > Y_noise,
    sensor(SensorId_insideTemp, temp),
    sensorValue(SensorId_insideTemp, X_temp_inside),
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    X_temp_inside == Y_temp,
    setOutsideEffectors(EffectorsNoise, 0).



%memberCheck(Element, List).
memberCheck(H,[H|_]).
memberCheck(H,[_|T]) :- memberCheck(H,T).