%Creates Figure E.3 - the absolute intergenerational mobility in the United
%States and in France for all adults and for different age groups. Requires
%results and data included in 'fr_us_ages.mat'

clear;
close all;
load('fr_us_ages.mat');

hhu2=plot(US1(:,1),US1(:,2),'-','color','k','linewidth',3);
hold on;
hhu1=plot(US2(:,1),US2(:,2),'-','color',[0.5 0.5 0.5],'linewidth',3);

hh4=fill(years_GGP,absmob_GGP_area,'k');
set(hh4,'facealpha',.1)
set(hh4,'linestyle','none')
hh1=plot(FR1(:,1),FR1(:,2),'k:','linewidth',3);
hh3=plot(FR2(1:3),FR2(4:6),'o:','linewidth',3);
set(hh3,'markerfacecolor',[0.5 0.5 0.5],'markeredgecolor',[0.5 0.5 0.5],'color',[0.5 0.5 0.6])

legend([hhu2,hhu1,hh1,hh3],'US - baseline','US - 30 year olds (Chetty et al. 2017)','France - Baseline','France - 20-39 year olds (Garbinti et al. 2018)','location','southwest');

legend('boxoff')
xlim([1940 1985]);
ylim([40 100])
set(gca,'xtick',1870:5:2000)
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
grid on

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500 400]);
exportgraphics(gcf,'figureE3.jpg','Resolution',1200)
exportgraphics(gcf,'figureE3.pdf')
exportgraphics(gcf,'figureE3.eps')
close all
clear