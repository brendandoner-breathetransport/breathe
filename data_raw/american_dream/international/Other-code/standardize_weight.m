function [x1,x2]=standardize_weight(y1,y2,w1,w2)

lim=1e8;
liml=1e7;

weight=w1;
N=sum(w1);
if (N>liml) && (N<lim)
    weight=round(weight);
    N=sum(weight);
else
    while N<liml
        weight=round(weight*2);
        N=sum(weight);
    end
    while N>lim
        weight=round(weight/2);
        N=sum(weight);
    end
    N=sum(weight);
end
NN=length(y1);
incs1=zeros(N,1);
count=1;
for i=1:NN
    incs1(count:count+weight(i)-1,1)=y1(i);
    count=count+weight(i);
end

weight=w2;
N=sum(w2);
if (N>liml) && (N<lim)
    weight=round(weight);
    N=sum(weight);
else
    while N<liml
        weight=round(weight*2);
        N=sum(weight);
    end
    while N>lim
        weight=round(weight/2);
        N=sum(weight);
    end
    N=sum(weight);
end
NN=length(y2);
incs2=zeros(N,1);
count=1;
for i=1:NN
    incs2(count:count+weight(i)-1,1)=y2(i);
    count=count+weight(i);
end

y1=incs1;
y2=incs2;

n1=length(y1);disp(n1)
n2=length(y2);disp(n2)
p1=randperm(n1);
p2=randperm(n2);
ll=min([n1 n2]);
x1=y1(p1(1:ll));
x2=y2(p2(1:ll));