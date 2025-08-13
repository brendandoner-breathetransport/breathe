%This script creates the results presented in Figure 8 in the appendix. It
%assumes a log-normal bivariate distribution for the joint income
%distribution of parents and children based on parameters for France (taken
%from 'France_Data_For_Decomposition.mat'), and then simulates discrete
%copulas at different resolutions to check whether the analytic result for
%the absolute mobility is recovered when discrete copulas are used.

clear
tic

load('France_Data_For_Decomposition.mat')

YY=1950;
i=find(years_top10share==YY);
mu1=mu(i);
mu2=mu(i+30);
sig1=sig(i);
sig2=sig(i+30);
rhoS=0.3;
rho=gaussian_theta(rhoS);
N=1e5;

fs=[10 20 40 50 80 100];
lfs=length(fs);
KL=10;

BBBB1=zeros(lfs+2,1);
BBBB1(1)=100*normcdf((mu2-mu1)./(sqrt(sig1^2+sig2^2-2*rho*sig1*sig2)));
for kkk=1:KL
    disp(kkk)
    w1=exp(mu1+sig1*randn(N,1));
    w2=exp(mu2+sig2*randn(N,1));
    AAAA=zeros(lfs+1,1);
    [w1,w2]=couple_vecs(w1,w2,rho,'gaussian');
    AAAA(1)=absmob0(w1,w2);
    for k=1:lfs
        f=fs(k);[C,tmp]=create_copula_N(w1,w2,f);AAAA(k+1)=absmob_with_copula(w1,w2,C);
    end
    BBBB1(2:end)=BBBB1(2:end)+AAAA/KL;
end

YY=1960;
i=find(years_top10share==YY);
mu1=mu(i);
mu2=mu(i+30);
sig1=sig(i);
sig2=sig(i+30);

BBBB2=zeros(lfs+2,1);
BBBB2(1)=100*normcdf((mu2-mu1)./(sqrt(sig1^2+sig2^2-2*rho*sig1*sig2)));
for kkk=1:KL
    disp(kkk)
    w1=exp(mu1+sig1*randn(N,1));
    w2=exp(mu2+sig2*randn(N,1));
    AAAA=zeros(lfs+1,1);
    [w1,w2]=couple_vecs(w1,w2,rho,'gaussian');
    AAAA(1)=absmob0(w1,w2);
    for k=1:lfs
        f=fs(k);[C,tmp]=create_copula_N(w1,w2,f);AAAA(k+1)=absmob_with_copula(w1,w2,C);
    end
    BBBB2(2:end)=BBBB2(2:end)+AAAA/KL;
end

YY=1970;
i=find(years_top10share==YY);
mu1=mu(i);
mu2=mu(i+30);
sig1=sig(i);
sig2=sig(i+30);

BBBB3=zeros(lfs+2,1);
BBBB3(1)=100*normcdf((mu2-mu1)./(sqrt(sig1^2+sig2^2-2*rho*sig1*sig2)));
for kkk=1:KL
    disp(kkk)
    w1=exp(mu1+sig1*randn(N,1));
    w2=exp(mu2+sig2*randn(N,1));
    AAAA=zeros(lfs+1,1);
    [w1,w2]=couple_vecs(w1,w2,rho,'gaussian');
    AAAA(1)=absmob0(w1,w2);
    for k=1:lfs
        f=fs(k);[C,tmp]=create_copula_N(w1,w2,f);AAAA(k+1)=absmob_with_copula(w1,w2,C);
    end
    BBBB3(2:end)=BBBB3(2:end)+AAAA/KL;
end

YY=1980;
i=find(years_top10share==YY);
mu1=mu(i);
mu2=mu(i+30);
sig1=sig(i);
sig2=sig(i+30);

BBBB4=zeros(lfs+2,1);
BBBB4(1)=100*normcdf((mu2-mu1)./(sqrt(sig1^2+sig2^2-2*rho*sig1*sig2)));
for kkk=1:KL
    disp(kkk)
    w1=exp(mu1+sig1*randn(N,1));
    w2=exp(mu2+sig2*randn(N,1));
    AAAA=zeros(lfs+1,1);
    [w1,w2]=couple_vecs(w1,w2,rho,'gaussian');
    AAAA(1)=absmob0(w1,w2);
    for k=1:lfs
        f=fs(k);[C,tmp]=create_copula_N(w1,w2,f);AAAA(k+1)=absmob_with_copula(w1,w2,C);
    end
    BBBB4(2:end)=BBBB4(2:end)+AAAA/KL;
end

%Export output
save('decomposition_check.mat')

toc