function vec=mobility_decompose(res)

vec=zeros(1,3);
vec(1)=100*res(1,2)/res(1,2)-100*res(end,2)/res(1,2);
tmp1=(100*res(1,3)/res(1,3)-100*res(end,3)/res(1,3));
tmp2=(100*res(1,4)/res(1,4)-100*res(end,4)/res(1,4));
vec(2)=tmp1*vec(1)/(tmp1+tmp2);
vec(3)=tmp2*vec(1)/(tmp1+tmp2);