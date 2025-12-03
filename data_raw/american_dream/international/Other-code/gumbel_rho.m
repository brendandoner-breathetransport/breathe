function rc=gumbel_rho(th)
load('theta_rankcorr.mat')
rc=interp1(theta,rankcorr,th,'pchip');