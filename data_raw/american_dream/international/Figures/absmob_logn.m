function A=absmob_logn(g,s1,s2,rho)
%Implements the bivariate log-normal model. Gets income growth, top
%10% income shares and intergenerational correlation as input and
%calculates the resulting absolute mobility
g=g/100;
s1=s1/100;
s2=s2/100;
sig1=norminv(0.9)-norminv(1-s1);
sig2=norminv(0.9)-norminv(1-s2);
mu1=0;
mu2=log(1+g)+sig1^2/2-sig2^2/2;
A=normcdf((mu2-mu1)./(sqrt(sig1^2+sig2^2-2*rho*sig1*sig2)));