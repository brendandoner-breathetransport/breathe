function rc=clayton_rho(th)
load('theta_rankcorr_clayton.mat')
rc=interp1(thetas,gg,th,'pchip');