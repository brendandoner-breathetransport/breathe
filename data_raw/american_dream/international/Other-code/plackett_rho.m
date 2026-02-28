function rc=plackett_rho(th)
% specifies the rank correlation in a Plackett copula given a parameter
% theta

load('theta_rankcorr_plackett.mat')
rc=interp1(thetas,gg,th,'pchip');