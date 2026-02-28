function a=absmob0(a1,a2)
% The basic code the calcaultes absolute mobility:
% Receives two vectors of the same size a1 and a2
% Returns the share (in percent) of elements in a2 that are higher than
% their respective (at the same location in the vector) elements in a1.

a=100*length(find((a2-a1)>0))/length(a1);