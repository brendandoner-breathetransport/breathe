function [w1,w2]=couple_vecs_plackett(s1,s2,theta)
% A function that gets two vectors of the same size s1 s2 as an input, as
% well as a parameter theta and returns the vectors as a matrix [w1,w2],
% where w1 has the elements of s1 and w2 has the elements of w2, with the
% joint rank distribution of w1 and w2 represented by a Plackett copula
% parameterized by theta.

N=length(s1);
u = plackett_rnd(theta,N);

ssss1=floor(tiedrank(u(:,1)));
ssss2=floor(tiedrank(u(:,2)));

indsss1=randperm(N);
tmp1=sort(s1(indsss1(1:N)));

indsss2=randperm(N);
tmp2=sort(s2(indsss2(1:N)));

w1=tmp1(ssss1);
w2=tmp2(ssss2);
[w1,tempind1]=sort(tmp1(ssss1));
w2=w2(tempind1);