%Creates Figure E.2 - Absolute intergenerational mobility in France using
%equal-split and individualized income data. Requires results and data
%included in 'france_equal_indiv.mat'

clear
close all
load('france_equal_indiv.mat');

h1=plot(yyy,equalsplit,'o:','linewidth',2);
hold on
h2=plot(yyy,indiv,'o:','linewidth',2);

set(h1,'markerfacecolor','k','markeredgecolor','k','color','k')
set(h2,'markerfacecolor',[0.5 0.5 0.5],'markeredgecolor',[0.5 0.5 0.5],'color',[0.5 0.5 0.5])

ddddd=legend([h1,h2],'Baseline (equal-split adults)','Individual adults','location','northeast');
legend('boxoff')
xlim([1970 1985]);
ylim([54 70])
set(gca,'xtick',1870:2:2000)
set(gca,'ytick',0:2:2000)
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
grid on

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500 400]);
exportgraphics(gcf,'figureE2.jpg','Resolution',1200)
exportgraphics(gcf,'figureE2.pdf')
exportgraphics(gcf,'figureE2.eps')
close all
clear