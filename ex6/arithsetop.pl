% Arithmetic operations

add(X,Y,Z):- Z is X+Y.
sub(X,Y,Z):- Z is X-Y.
mul(X,Y,Z):- Z is X*Y.
div(X,Y,Z):- Z is X/Y.
mod(X,Y,Z):- Z is X mod Y.
max(X,Y,X):- X>=Y.
max(X,Y,Y):- Y>X.

% Set operations

member(X,[X|_]).
member(X,[_|T]):- member(X,T).

union([],L,L).
union([H|T],L,R):- member(H,L),union(T,L,R).
union([H|T],L,[H|R]):- \+member(H,L),union(T,L,R).

intersection([],_,[]).
intersection([H|T],L,[H|R]):- member(H,L),intersection(T,L,R).
intersection([_|T],L,R):- intersection(T,L,R).

difference([],_,[]).
difference([H|T],L,R):- member(H,L),difference(T,L,R).
difference([H|T],L,[H|R]):- \+member(H,L),difference(T,L,R).
