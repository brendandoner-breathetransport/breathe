%Creates Figure 2
%This figure uses data on mobility measures from multiple copulas found the
%literature. The mobility measures are:
%1. Spearman's rank correlation (variable r)
%2. Bartholomew's index (variable b)
%3. Ave. non-zero absolute jump (variable j)
%4. Shorrocks' trace index (variable tr)
% The variables are taken from the data file 'copulas_measures.mat'
%
% Each variable has 28 values, based on 28 copulas, in the following order
%1. Denmark 1 (source: Jantti et al (2006))
%2. Finland 1 (source: Jantti et al (2006))
%3. Germany 1 (source: Eberharter (2014))
%4. Norway 1 (source: Jantti et al (2006))
%5. Sweden 1 (source: Jantti et al (2006))
%6. UK 1 (source: Eberharter (2014))
%7. UK 2 (source: Jantti et al (2006))
%8. USA 1 (source: Chetty et al (2017))
%9. USA 2 (source: Eberharter (2014))
%10. USA 3 (source: Jantti et al (2006))
%11. Denmark 2 (source: Jantti et al (2006))
%12. Denmark 3 (source: Jantti et al (2006))
%13. Denmark 4 (source: Jantti et al (2006))
%14. Finland 2 (source: Jantti et al (2006))
%15. Finland 3 (source: Jantti et al (2006))
%16. Finland 4 (source: Jantti et al (2006))
%17. Norway 2 (source: Jantti et al (2006))
%18. Norway 3 (source: Jantti et al (2006))
%19. Norway 4 (source: Jantti et al (2006))
%20. Sweden 2 (source: Jantti et al (2006))
%21. Sweden 3 (source: Jantti et al (2006))
%22. Sweden 4 (source: Jantti et al (2006))
%23. UK 3 (source: Jantti et al (2006))
%24. UK 4 (source: Jantti et al (2006))
%25. UK 5 (source: Jantti et al (2006))
%26. USA 4 (source: Jantti et al (2006))
%27. USA 5 (source: Jantti et al (2006))
%28. USA 6 (source: Jantti et al (2006))

clear
close all
load('copulas_measures.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

% Six top panels - plotting the four measures one against the other
subplot(4,3,1);
h=plot(b,r,'ko','linewidth',2);
set(h,'MarkerFaceColor',blue)
set(h,'markersize',7)
title(['\rho=' num2str(corr(b,r,'type','pearson'),2)]);
xlabel('Bartholomew''s index','fontsize',9)
ylabel('Rank correlation','fontsize',9)
set(gca,'fontsize',9)
box off
grid on

subplot(4,3,2);
h=plot(j,r,'ko','linewidth',2);
set(h,'MarkerFaceColor',blue)
set(h,'markersize',7)
title(['\rho=' num2str(corr(j,r,'type','pearson'),2)]);
xlabel('Ave. non-zero absolute jump','fontsize',9)
ylabel('Rank correlation','fontsize',9)
set(gca,'fontsize',9)
box off
grid on

subplot(4,3,3);
h=plot(tr,r,'ko','linewidth',2);
set(h,'MarkerFaceColor',blue)
set(h,'markersize',7)
title(['\rho=' num2str(corr(tr,r,'type','pearson'),2)]);
xlabel('Shorrocks'' trace index','fontsize',9)
ylabel('Rank correlation','fontsize',9)
set(gca,'fontsize',9)
xlim([0.8 1]);
xticks(0.8:0.05:1);
box off
grid on

subplot(4,3,4);
h=plot(b,tr,'ko','linewidth',2);
set(h,'MarkerFaceColor',blue)
set(h,'markersize',7)
title(['\rho=' num2str(corr(b,tr,'type','pearson'),2)]);
xlabel('Bartholomew''s index','fontsize',9)
ylabel('Shorrocks'' trace index','fontsize',9)
set(gca,'fontsize',9)
box off
grid on

subplot(4,3,5);
h=plot(b,j,'ko','linewidth',2);
set(h,'MarkerFaceColor',blue)
set(h,'markersize',7)
title(['\rho=' num2str(corr(b,j,'type','pearson'),2)]);
xlabel('Bartholomew''s index','fontsize',9)
ylabel('Ave. non-zero absolute jump','fontsize',9)
set(gca,'fontsize',9)
box off
grid on

subplot(4,3,6);
h=plot(tr,j,'ko','linewidth',2);
set(h,'MarkerFaceColor',blue)
set(h,'markersize',7)
title(['\rho=' num2str(corr(tr,j,'type','pearson'),2)]);
xlabel('Shorrocks'' trace index','fontsize',9)
ylabel('Ave. non-zero absolute jump','fontsize',9)
set(gca,'fontsize',9)
xlim([0.8 1]);
xticks(0.8:0.05:1);
box off
grid on

% Bottom panel - 'figure2_results.mat' includes the calculation results.
% 'abs_mobility' includes the baseline absolute mobility estimates of Chetty et al. (2017)
% 'results' includes results of a calculation in which the marginal
% distributions in years that are 30 years apart were matched using the
% copulas considered above, as explained in detail in the readme file
load('figure2_results.mat')

subplot(4,3,7:12)

hh4=fill([years fliplr(years)]',[min(100*results') (fliplr(max(100*results')))],'r');
set(hh4,'facecolor',blue);
set(hh4,'facealpha',.2)

set(hh4,'linestyle','none')
hold on;
h1=plot(years_mobility,abs_mobility,'ok-','markersize',6,'markerfacecolor','k','linewidth',2);
h2=plot(1940:1980,mean(100*results'),'-.','color',blue,'linewidth',3);

xlim([1940 1980])
legend([h1,h2],'Chetty et al.','Average of empirical copulas estimates')
ylabel('Pct. of children earning more than their parents','fontsize',9)
xlabel('Cohort','fontsize',9)
set(gca,'fontsize',9)

legend boxoff
box off
set(gca, 'YGrid', 'on', 'XGrid', 'off')
ylim([50 100])

%Export figure
set(gcf, 'Position', [10 10 500*1.8 400*1.8]);
set(gcf,'color','w');
exportgraphics(gcf,'figure2.jpg','Resolution',1200)
exportgraphics(gcf,'figure2.pdf')
exportgraphics(gcf,'figure2.eps')
close all
clear