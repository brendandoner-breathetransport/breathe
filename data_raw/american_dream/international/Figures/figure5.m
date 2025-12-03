%Creates Figure 5 - counterfactual calculations of absolute mobility in Australia, France, Japan, and the United States after 1940
%The results are included in 'counterfactual_results.mat'

clear
close all
load('counterfactual_results.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

subplot(2,2,1)
hh1=plot(AU(:,1),100*AU(:,2)/AU(1,2),'-','color',black,'linewidth',3);
hold on;
hh2=plot(AU(:,1),100*AU(:,3)/AU(1,3),'-.','color',darkred,'linewidth',3);
hh3=plot(AU(:,1),100*AU(:,4)/AU(1,4),':','color',blue,'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest');
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort');
ylabel('Abs. mobility, first cohort = 100%');
legend boxoff
title('Australia')
set(gca, 'YGrid', 'on', 'XGrid', 'off')

subplot(2,2,2)
hh1=plot(FR(:,1),100*FR(:,2)/FR(find(FR(:,1)==1940),2),'-','color',black,'linewidth',3);
hold on;
hh2=plot(FR(:,1),100*FR(:,3)/FR(find(FR(:,1)==1940),3),'-.','color',darkred,'linewidth',3);
hh3=plot(FR(:,1),100*FR(:,4)/FR(find(FR(:,1)==1940),4),':','color',blue,'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest')
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort');
ylabel('Abs. mobility, first cohort = 100%');
legend boxoff
title('France')
set(gca, 'YGrid', 'on', 'XGrid', 'off')

subplot(2,2,3)
hh1=plot(JP(:,1),100*JP(:,2)/JP(find(JP(:,1)==1947),2),'-','color',black,'linewidth',3);
hold on;
hh2=plot(JP(:,1),100*JP(:,3)/JP(find(JP(:,1)==1947),3),'-.','color',darkred,'linewidth',3);
hh3=plot(JP(:,1),100*JP(:,4)/JP(find(JP(:,1)==1947),4),':','color',blue,'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest')
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort');
ylabel('Abs. mobility, first cohort = 100%');
legend boxoff
title('Japan')
set(gca, 'YGrid', 'on', 'XGrid', 'off')

subplot(2,2,4)
hh1=plot(US(:,1),100*US(:,2)/US(find(US(:,1)==1940),2),'-','color',black,'linewidth',3);
hold on;
hh2=plot(US(:,1),100*US(:,3)/US(find(US(:,1)==1940),3),'-.','color',darkred,'linewidth',3);
hh3=plot(US(:,1),100*US(:,4)/US(find(US(:,1)==1940),4),':','color',blue,'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest')
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort');
ylabel('Abs. mobility, first cohort = 100%');
legend boxoff
title('United States')
set(gca, 'YGrid', 'on', 'XGrid', 'off')

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [50 50 500*1.8 400*2]);
exportgraphics(gcf,'figure5.jpg','Resolution',1200)
exportgraphics(gcf,'figure5.pdf')
exportgraphics(gcf,'figure5.eps')
close all
clear