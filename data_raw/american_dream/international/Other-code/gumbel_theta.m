function th=gumbel_theta(rc)
load('theta_rankcorr.mat')
th=interp1(rankcorr,theta,rc,'pchip');