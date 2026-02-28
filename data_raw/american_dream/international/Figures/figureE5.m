%Creates Figure E.5 - absolute intergenerational mobility in France and the
%United States for total income and labor income. This script creates the
%plot using 'baseline_labor.mat'.

clear;
close all;
load('baseline_labor.mat');

grey1=[0.4 0.4 0.4];
grey2=[0.8 0.8 0.8];
grey3=[0.8 0.8 0.8];
grey4=[0.5 0.5 0.5];

hh1=plot(usa_baseline_years,usa_baseline,'-','color','k','linewidth',3);
hold on
hh2=plot(usa_labor_years,usa_labor,'-','color',[0.5 0.5 0.5],'linewidth',3);
h1=plot(fr_baseline_years,fr_baseline,':','linewidth',3);
h2=plot(fr_labor_years,fr_labor,':','linewidth',3);

set(h1,'markerfacecolor','k','markeredgecolor','k','color','k')
set(h2,'markerfacecolor',[0.5 0.5 0.5],'markeredgecolor',[0.5 0.5 0.5],'color',[0.5 0.5 0.5])

grid off;
ddddd=legend([hh1,hh2,h1,h2],'US - baseline','US - labor income','France - baseline','France - labor income','location','northeast');
legend('boxoff')
xlim([1960 1985]);
ylim([50 75])
set(gca,'xtick',1870:5:2000)
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
grid on

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500 400]);
exportgraphics(gcf,'figureE5.jpg','Resolution',1200)
exportgraphics(gcf,'figureE5.pdf')
exportgraphics(gcf,'figureE5.eps')
close all
clear