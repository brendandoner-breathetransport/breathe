%Creates Figure E.8 - absolute mobility with mis-estimation of inequality in
%Japan and the United States and growth in Japan and France of inequality
%changes and income growth. This script creates the plot using
%'tweaks_over_time.mat'.

clear;
close all;
load('tweaks_over_time.mat')

subplot(2,2,1)

h1=plot(JP_years,JP1_1,'k','linewidth',2);
hold on
h2=plot(JP_years,JP1_2,'--k','linewidth',2);
h3=plot(JP_years,JP1_3,':k','linewidth',2);

ylim([40 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:5:100])
legend([h1,h2,h3],'Baseline','10% inequality growth underestimation','10% inequality growth overestimation','location','southwest')
legend boxoff
xlabel('Cohort');
ylabel('Absolute mobility (%)');
title('Japan')
grid on
box off

subplot(2,2,2)

h1=plot(US_years,US1_1,'color',[0, 0.4470, 0.7410],'linewidth',2);
hold on
h2=plot(US_years,US1_2,'--','color',[0, 0.4470, 0.7410],'linewidth',2);
h3=plot(US_years,US1_3,':','color',[0, 0.4470, 0.7410],'linewidth',2);

ylim([40 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:5:100])
legend([h1,h2,h3],'Baseline','10% inequality growth underestimation','10% inequality growth overestimation','location','southwest')
legend boxoff
xlabel('Cohort');
ylabel('Absolute mobility (%)');
title('United States')
grid on
box off

subplot(2,2,3)

h1=plot(JP_years,JP2_1,'k','linewidth',2);
hold on
h2=plot(JP_years,JP2_2,'--k','linewidth',2);
h3=plot(JP_years,JP2_3,':k','linewidth',2);

ylim([40 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:5:100])
legend([h1,h2,h3],'Baseline','10% income growth underestimation','10% income growth overestimation','location','southwest')
legend boxoff
xlabel('Cohort');
ylabel('Absolute mobility (%)');
title('Japan')
grid on
box off

subplot(2,2,4)

h1=plot(FR_years,FR2_1,'color',[0, 0.4470, 0.7410],'linewidth',2);
hold on
h2=plot(FR_years,FR2_2,'--','color',[0, 0.4470, 0.7410],'linewidth',2);
h3=plot(FR_years,FR2_3,':','color',[0, 0.4470, 0.7410],'linewidth',2);

ylim([40 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:5:100])
legend([h1,h2,h3],'Baseline','10% income growth underestimation','10% income growth overestimation','location','southwest')
legend boxoff
xlabel('Cohort');
ylabel('Absolute mobility (%)');
title('France')
grid on
box off

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*2 400*2]);
exportgraphics(gcf,'figureE8.jpg','Resolution',1200)
exportgraphics(gcf,'figureE8.pdf')
exportgraphics(gcf,'figureE8.eps')
close all
clear