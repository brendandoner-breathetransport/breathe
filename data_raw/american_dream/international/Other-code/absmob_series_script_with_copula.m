%This script imports a table of income samples of the same size, calculates
%and plots a series of absolute mobility values.
%
%It uses an example data file - samples.csv - that contains simulated
%samples that are based on parameters which represent data for the years
%1915-2014 in France.
%
%The script also imports a copula - in this example a 10x10 matrix that is
%based on a copula esimtated for the United States in Chetty et al. (2017).
%It then uses the function absmob_with_copula that implements equation 3.1
%in the paper.

clear
close all

% Import samples
A=importdata('samples.csv');
years=A(1,:);
samps=A(2:end,:);
n=length(years);

% Import copula
C=importdata('copula_example.csv');

%Rank correlation value
rankcorr=0.3;

% Results vector
absmobility=zeros(n-30,1);

for i=1:n-30
    % Match samples with a modelled copula: other options other than Gumbel
    % exist (see Appendix C)
    %[w1,w2]=couple_vecs(samps(:,i),samps(:,i+30),gumbel_theta(rankcorr),'gumbel');
    
    
    % Calculate the measure of absolute mobility for the matched samples w1
    % and w2
    absmobility(i)=absmob_with_copula(samps(:,i),samps(:,i+30),C);
end

% plot results
h1=plot(years(1:end-30),absmobility,'ko:','linewidth',1);
set(h1,'markerfacecolor','k','markersize',3)

ylim([0 100])
box off
ylabel('Absolute mobility (%)')
xlabel('Cohort')
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500 400]);
exportgraphics(gcf,'absmob_series_with_copula.jpg','Resolution',1200)
close all
clear