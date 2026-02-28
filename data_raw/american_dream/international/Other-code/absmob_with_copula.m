function a=absmob_with_copula(w1,w2,C)
% The basic code the calcaultes absolute mobility with a given matrix:
% Receives two vectors of the same size w1 and w2 as well as a discrete
% copula C.
% Returns the share (in percent) of elements in w2 that are higher than
% their respective (at the same location in the vector) elements in w1,
% given that the joint rank distribution is described in C.

f=length(C(:,1));
delta=1/f;
pp=delta/2:delta:1;
a=0;
for ii=1:f
    for jj=1:f
        a=a+(sign(quantile(w2,pp(jj))-quantile(w1,pp(ii)))+1)/2*C(ii,jj);
    end
end
a=100*a/f;