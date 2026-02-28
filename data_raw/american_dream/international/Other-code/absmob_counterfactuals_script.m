%This script imports a table of income samples of the same size, calculates
%and plots a series of absolute mobility values with two counterfactual
%scenarios - fixed distribution and fixed income growth (see Section 4.3)
%
%It uses an example data file - samples.csv - that contains simulated
%samples that are based on parameters which represent data for the years
%1915-2014 in France.
%
%The script also uses three other functions: gumbel_theta, that transforms
%a rank correlation to the Gumbel copula parameter; couple_vecs, that
%matches together two vectors using a modeled copula; absmob0, a function
%that receives two matched vectors of the same size and returns the
%resulting absolute mobility.

clear
close all

darkred=[0.635 0.078 0.184];
blue=[0 0.447 0.741];

% Import samples
A=importdata('samples.csv');

% We consider only the later part of the period to demonstrate the
% decomposition, as described in Section 4.3
A=A(:,30:end);

years=A(1,:);
samps=A(2:end,:);
n=length(years);

% Calculate the average annual income growth rate over the entire period
average_incomes=mean(samps);
average_growth_rate=(average_incomes(end)/average_incomes(1))^(1/(n-1))-1;

% Create counterfactual samples
counter1=samps;
counter2=samps;
for i=2:n
    % First counterfactual: fixed distribution shape
    counter1(:,i)=counter1(:,1)/mean(counter1(:,1))*average_incomes(i);
    
    % Second counterfactual: actual distribution, average income determined
    % by a constant growth rate
    counter2(:,i)=counter2(:,i)/mean(counter2(:,i))*mean(counter2(:,i-1))*(1+average_growth_rate);
end

%Rank correlation value
rankcorr=0.3;

% Results vector
absmobility=zeros(n-30,3);

for i=1:n-30
    % Baseline
    [w1,w2]=couple_vecs(samps(:,i),samps(:,i+30),gumbel_theta(rankcorr),'gumbel');
    absmobility(i,1)=absmob0(w1,w2);
    
    % Counterfactual 1
    [w1,w2]=couple_vecs(counter1(:,i),counter1(:,i+30),gumbel_theta(rankcorr),'gumbel');
    absmobility(i,2)=absmob0(w1,w2);
    
    % Counterfactual 2
    [w1,w2]=couple_vecs(counter2(:,i),counter2(:,i+30),gumbel_theta(rankcorr),'gumbel');
    absmobility(i,3)=absmob0(w1,w2);
end

% plot results
h1=plot(years(1:end-30),absmobility(:,1),'ko:','linewidth',1);
hold on
set(h1,'markerfacecolor','k','markersize',3)
h2=plot(years(1:end-30),absmobility(:,2),'+:','linewidth',1);
set(h2,'markerfacecolor',blue,'markersize',4,'color',blue)
h3=plot(years(1:end-30),absmobility(:,3),'^:','linewidth',1);
set(h3,'markerfacecolor','k','markersize',3)
set(h3,'markerfacecolor',darkred,'markersize',3,'color',darkred)

legend([h1,h2,h3],'Baseline','Counterfactual 1 - fixed inequality','Counterfactual 2 - fixed growth','location','southwest')
legend boxoff

ylim([0 100])
box off
ylabel('Absolute mobility (%)')
xlabel('Cohort')
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500 400]);
exportgraphics(gcf,'absmob_decomposition.jpg','Resolution',1200)
close all
clear