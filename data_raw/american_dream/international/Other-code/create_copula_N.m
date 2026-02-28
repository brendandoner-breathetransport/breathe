function [C,tmp]=create_copula_N(a,b,N)
%a and b are assumed vectors of length n
%N is the number quantiles. For percentiles it is 100, for qunitiles 5,
%etc. One restriction is that n/N is integer.

n=length(a);
step=n/N;

tmp=zeros(n,4);
tmp(:,1)=a;
tmp(:,3)=b;

tmp=sortrows(tmp,1);
for i=1:N
    tmp(step*(i-1)+1:i*step,2)=i;
end
tmp=sortrows(tmp,3);
for i=1:N
    tmp(step*(i-1)+1:i*step,4)=i;
end

C=zeros(N,N);
for i=1:N
    for j=1:N
        indind=intersect(find(tmp(:,2)==i),find(tmp(:,4)==j));
        C(i,j)=(1/step)*length(indind);
    end
end

tmp=sortrows(tmp,1);