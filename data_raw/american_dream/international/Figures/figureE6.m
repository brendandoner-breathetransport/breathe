%Creates Figure E.6 - absolute intergenerational mobility in France and the
%United States for pre-tax and post-tax income. This script creates the
%plot using 'pre_post_res.mat'.

clear;
close all;
load('pre_post_res.mat');

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

subplot(1,2,1)

h1=plot(fr_years,fr_baseline,'-','color',black,'linewidth',3);
hold on
h2=plot(fr_years,fr_posttax,'-.','color',darkred,'linewidth',3);

xlim([1910 1990]);
ylim([50 100]);
set(gca,'ytick',0:5:200)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
legend boxoff
title('France')
set(gca, 'YGrid', 'on', 'XGrid', 'off')
legend([h1,h2],'Baseline (pre-tax)','Post-tax','location','southwest')
legend boxoff

subplot(1,2,2)

h1=plot(us_years,us_baseline,'-','color',black,'linewidth',3);
hold on
h2=plot(us_years,us_posttax,'-.','color',darkred,'linewidth',3);

xlim([1910 1990]);
ylim([50 100]);
set(gca,'ytick',0:5:200)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
legend boxoff
title('United States')
set(gca, 'YGrid', 'on', 'XGrid', 'off')
legend([h1,h2],'Baseline (pre-tax)','Post-tax','location','southwest')
legend boxoff

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*1.8 400]);
exportgraphics(gcf,'figureE6.jpg','Resolution',1200)
exportgraphics(gcf,'figureE6.pdf')
exportgraphics(gcf,'figureE6.eps')
close all
clear