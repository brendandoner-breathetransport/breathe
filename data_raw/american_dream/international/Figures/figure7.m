%Creates Figure 7 - absolute mobility in France under the bivariate log-normal approximation
%The results are included in 'FR_inequality_measures_results.mat'

clear
close all
load('FR_inequality_measures_results.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

h1=plot(FR_inequality_measures(:,1),FR_inequality_measures(:,2),'k-','linewidth',3);
hold on;
h2=plot(FR_inequality_measures(:,1),FR_inequality_measures(:,3),'k-','linewidth',2);
h3=plot(FR_inequality_measures(:,1),FR_inequality_measures(:,4),'k-','linewidth',2);
h4=plot(FR_inequality_measures(:,1),FR_inequality_measures(:,5),'k-','linewidth',2);
h5=plot(FR_inequality_measures(:,1),FR_inequality_measures(:,6),'k+-','linewidth',1);

set(h2,'color',darkred,'linestyle','-.')
set(h3,'color',blue,'linestyle',':')
set(h4,'color',purple,'linestyle','--')
set(h5,'color',grey)
legend([h1,h2,h3,h4,h5],'Baseline','Bottom 50%','Top 10%','Top 1%','Gini','location','northeast')
legend boxoff

xlim([1910 1990]);
ylim([50 100]);set(gca,'ytick',50:5:100)
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
grid on

set(gca, 'YGrid', 'on', 'XGrid', 'off')
set(gcf,'color','w');
set(gcf, 'Position', [80 80 500 400]);

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500 400]);
exportgraphics(gcf,'figure7.jpg','Resolution',1200)
exportgraphics(gcf,'figure7.pdf')
exportgraphics(gcf,'figure7.eps')
close all
clear