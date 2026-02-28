function th=plackett_theta(rc)
% specifies the Plackett copula parameter given rank correlation rc

load('theta_rankcorr_plackett.mat')
th=interp1(gg,thetas,rc,'pchip');