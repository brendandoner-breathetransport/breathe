function [x err]=moving_average(data,num)

n=length(data);
x=zeros(n,1);
for i=1:n
    ind=(i-num:i+num);
    ind(ind<=0)=[];
    ind(ind>n)=[];
    fac=1/sqrt(length(ind)-1);
    x(i)=mean(data(ind));
    err(i)=fac*std(data(ind));
end