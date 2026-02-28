function th=clayton_theta(rc)
load('theta_rankcorr_clayton.mat')
th=interp1(gg,thetas,rc,'pchip');