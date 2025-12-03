%This script creates the main results presented in Figure 18 in the
%appendix. It estimates absolute mobility for the United States given
%multiple adjustments to income definition and unit of observation using the
%CPS data (taken from 'CPS_workspace.mat'). Additional workspaces and
%scripts used by this script are also included in the folder.

clear
close all
load('CPS_workspace.mat')

ageroup=[30 40];

ind1=intersect(find(AGE>=18),find(AGE<=100));
ind2=intersect(find(AGE>=ageroup(1)),find(AGE<=ageroup(1)));
ind3=intersect(find(AGE>=ageroup(2)),find(AGE<=ageroup(2)));
ind4=intersect(find(AGE>=35),find(AGE<=45));
NY=length(YEARS);

absm1=zeros(7,NY-30);
rho=0.3;

for i=1:NY-30
    indyear1=find(YEAR==YEARS(i));
    indyear2=find(YEAR==(YEARS(i)+30));
    
    inc1=INCTOT(intersect(indyear1,ind1))/defl2(i);
    inc2=INCTOT(intersect(indyear2,ind1))/defl2(i+30);
    w1=ASECWT(intersect(indyear1,ind1));
    w2=ASECWT(intersect(indyear2,ind1));
    [inc1,inc2]=standardize_weight(inc1,inc2,w1,w2);
    
    inc1h=INCTOT(intersect(indyear1,ind4))/defl2(i);
    inc2h=INCTOT(intersect(indyear2,ind4))/defl2(i+30);
    SER1=SERIAL(intersect(indyear1,ind4));
    SER2=SERIAL(intersect(indyear2,ind4));
    w1h=ASECWTH(intersect(indyear1,ind4));
    w2h=ASECWTH(intersect(indyear2,ind4));
    [inc1h,w1h]=make_hincome1(inc1h,w1h,SER1);
    [inc2h,w2h]=make_hincome1(inc2h,w2h,SER2);
    [inc1h,inc2h]=standardize_weight(inc1h,inc2h,w1h,w2h);
    
    inc1h1=INCTOT(intersect(indyear1,ind1))/defl2(i);
    inc2h1=INCTOT(intersect(indyear2,ind1))/defl2(i+30);
    SER1=SERIAL(intersect(indyear1,ind1));
    SER2=SERIAL(intersect(indyear2,ind1));
    w1h1=ASECWTH(intersect(indyear1,ind1));
    w2h1=ASECWTH(intersect(indyear2,ind1));
    [inc1h1,w1h1]=make_hincome2(inc1h1,w1h1,SER1);
    [inc2h1,w2h1]=make_hincome2(inc2h1,w2h1,SER2);
    [inc1h1,inc2h1]=standardize_weight(inc1h1,inc2h1,w1h1,w2h1);
    
    inc1h2=INCTOT(intersect(indyear1,ind4))/defl2(i);
    inc2h2=INCTOT(intersect(indyear2,ind4))/defl2(i+30);
    SER1=SERIAL(intersect(indyear1,ind4));
    SER2=SERIAL(intersect(indyear2,ind4));
    w1h2=ASECWTH(intersect(indyear1,ind4));
    w2h2=ASECWTH(intersect(indyear2,ind4));
    [inc1h2,w1h2]=make_hincome2(inc1h2,w1h2,SER1);
    [inc2h2,w2h2]=make_hincome2(inc2h2,w2h2,SER2);
    [inc1h2,inc2h2]=standardize_weight(inc1h2,inc2h2,w1h2,w2h2);
    
    inc1a=INCTOT(intersect(indyear1,ind2))/defl2(i);
    inc2a=INCTOT(intersect(indyear2,ind2))/defl2(i+30);
    w1a=ASECWT(intersect(indyear1,ind2));
    w2a=ASECWT(intersect(indyear2,ind2));
    [inc1a,inc2a]=standardize_weight(inc1a,inc2a,w1a,w2a);
    
    inc1b=INCTOT(intersect(indyear1,ind3))/defl2(i);
    inc2b=INCTOT(intersect(indyear2,ind3))/defl2(i+30);
    w1b=ASECWT(intersect(indyear1,ind3));
    w2b=ASECWT(intersect(indyear2,ind3));
    [inc1b,inc2b]=standardize_weight(inc1b,inc2b,w1b,w2b);
    
    inc1c=INCTOT(intersect(indyear1,ind2))/defl2(i);
    inc2c=INCTOT(intersect(indyear2,ind3))/defl2(i+30);
    w1c=ASECWT(intersect(indyear1,ind2));
    w2c=ASECWT(intersect(indyear2,ind3));
    [inc1c,inc2c]=standardize_weight(inc1c,inc2c,w1c,w2c);
    
    [w1,w2]=couple_vecs(inc1,inc2,gumbel_theta(rho),'gumbel');
    absm1(1,i)=absmob0(w1,w2);
    
    [w1,w2]=couple_vecs(inc1a,inc2a,gumbel_theta(rho),'gumbel');
    absm1(2,i)=absmob0(w1,w2);
    
    [w1,w2]=couple_vecs(inc1b,inc2b,gumbel_theta(rho),'gumbel');
    absm1(3,i)=absmob0(w1,w2);
    
    [w1,w2]=couple_vecs(inc1h,inc2h,gumbel_theta(rho),'gumbel');
    absm1(4,i)=absmob0(w1,w2);
    
    [w1,w2]=couple_vecs(inc1h1,inc2h1,gumbel_theta(rho),'gumbel');
    absm1(5,i)=absmob0(w1,w2);
    
    [w1,w2]=couple_vecs(inc1h2,inc2h2,gumbel_theta(rho),'gumbel');
    absm1(6,i)=absmob0(w1,w2);
    
    [w1,w2]=couple_vecs(inc1c,inc2c,gumbel_theta(rho),'gumbel');
    absm1(7,i)=absmob0(w1,w2);
end
absm=absm1';
YEARS=YEARS(1:end-30);