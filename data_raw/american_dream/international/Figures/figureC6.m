%Creates Figure C.6 - The decrease in absolute mobility in Australia,
%France, Japan and the United States with different thresholds. Requires
%results and data included in 'limits.mat'

clear;
close all;
load('limits.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

subplot(2,2,1)

h1=plot(AU(:,1),AU(:,2),'k','linewidth',2);
hold on
h2=plot(AU(:,1),AU(:,3),'k--','linewidth',2);
h3=plot(AU(:,1),AU(:,4),'k:','linewidth',2);
h4=plot(AU(:,1),AU(:,5),'-.','color',blue,'linewidth',1);
h5=plot(AU(:,1),AU(:,6),'--','color',darkred,'linewidth',1);

ylim([0 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:10:100])
legend([h1,h2,h3],'Absolute mobility (\epsilon more than parents) (%)','At least 10% more than parents (%)','More than parents by at least av. growth (%)','location','southwest')
legend boxoff

xlabel('Cohort');
title('Australia')
grid on
box off

subplot(2,2,2)

h1=plot(FR(:,1),FR(:,2),'k','linewidth',2);
hold on
h2=plot(FR(:,1),FR(:,3),'k--','linewidth',2);
h3=plot(FR(:,1),FR(:,4),'k:','linewidth',2);
h4=plot(FR(:,1),FR(:,5),'-.','color',blue,'linewidth',1);
h5=plot(FR(:,1),FR(:,6),'--','color',darkred,'linewidth',1);

ylim([0 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:10:100])
legend([h1,h2,h3],'Absolute mobility (\epsilon more than parents) (%)','At least 10% more than parents (%)','More than parents by at least av. growth (%)','location','southwest')
legend boxoff

xlabel('Cohort');
title('France')
grid on
box off

subplot(2,2,3)

h1=plot(JP(:,1),JP(:,2),'k','linewidth',2);
hold on
h2=plot(JP(:,1),JP(:,3),'k--','linewidth',2);
h3=plot(JP(:,1),JP(:,4),'k:','linewidth',2);
h4=plot(JP(:,1),JP(:,5),'-.','color',blue,'linewidth',1);
h5=plot(JP(:,1),JP(:,6),'--','color',darkred,'linewidth',1);

ylim([0 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:10:100])
legend([h1,h2,h3],'Absolute mobility (\epsilon more than parents) (%)','At least 10% more than parents (%)','More than parents by at least av. growth (%)','location','southwest')
legend boxoff

xlabel('Cohort');
title('Japan')
grid on
box off

subplot(2,2,4)

h1=plot(US(:,1),US(:,2),'k','linewidth',2);
hold on
h2=plot(US(:,1),US(:,3),'k--','linewidth',2);
h3=plot(US(:,1),US(:,4),'k:','linewidth',2);
h4=plot(US(:,1),US(:,5),'-.','color',blue,'linewidth',1);
h5=plot(US(:,1),US(:,6),'--','color',darkred,'linewidth',1);

ylim([0 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:10:100])
legend([h1,h2,h3],'Absolute mobility (\epsilon more than parents) (%)','At least 10% more than parents (%)','More than parents by at least av. growth (%)','location','southwest')
legend boxoff

xlabel('Cohort');
title('United States')
grid on
box off

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [100 100 500*2 400*2]);
exportgraphics(gcf,'figureC6.jpg','Resolution',1200)
exportgraphics(gcf,'figureC6.pdf')
exportgraphics(gcf,'figureC6.eps')
close all
clear