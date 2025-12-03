function [inc,wei]=make_hincome2(p_incs,WT,SERIAL)

se=unique(SERIAL);
n=length(se);
inc=zeros(n,1);
wei=zeros(n,1);
for i=1:n
    ind=find(SERIAL==se(i));
    inc(i)=sum(p_incs(ind));
    wei(i)=WT(ind(1));
end