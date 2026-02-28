%Creates Figure 6 - counterfactual calculations of absolute mobility in the United States before 1940
%The results are included in 'counterfactual_results_US_early.mat'

clear
close all
load('counterfactual_results_US_early.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

hh1=plot(US(:,1),100*US(:,2)/US(1,2),'-','color',black,'linewidth',3);
hold on;
hh2=plot(US(:,1),100*US(:,3)/US(1,3),'-.','color',darkred,'linewidth',3);
hh3=plot(US(:,1),100*US(:,4)/US(1,4),':','color',blue,'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','northwest')
xlim([1915 1940]);
ylim([95 135]);
set(gca,'ytick',0:5:200)
set(gca,'xtick',1915:5:2000)
box off;
xlabel('Cohort');
ylabel('Abs. mobility, first cohort = 100%');
legend boxoff
set(gca, 'YGrid', 'on', 'XGrid', 'off')

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500 400]);
exportgraphics(gcf,'figure6.jpg','Resolution',1200)
exportgraphics(gcf,'figure6.pdf')
exportgraphics(gcf,'figure6.eps')
close all
clear