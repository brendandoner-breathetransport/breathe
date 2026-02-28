%Creates Figure 4 - main results
%The results, similar to those detailed in Table 3 in the Appendix are
%included in 'main results.mat'

clear
close all
load('main_results.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

subplot(1,2,1)

h1=plot(AU(:,1),AU(:,2),'-','color',black,'linewidth',2);
hold on;
h2=plot(CA(:,1),CA(:,2),'-.','color',darkred,'linewidth',2);
h3=plot(DK(:,1),DK(:,2),':','color',blue,'linewidth',2);
h4=plot(FI(:,1),FI(:,2),'--','color',purple,'linewidth',2);
h5=plot(FR(:,1),FR(:,2),'+-','markersize',5,'markerfacecolor',grey,'color',grey,'linewidth',1);

xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:5:100);
set(gca,'xtick',1870:10:2000)
box off;
legend([h1,h2,h3,h4,h5],'Australia','Canada','Denmark','Finland','France','location','south')
legend boxoff
xlabel('Cohort');
ylabel('Absolute mobility (%)');
set(gca, 'YGrid', 'on', 'XGrid', 'off')

subplot(1,2,2)

h1=plot(JP(:,1),JP(:,2),'-','color',black,'linewidth',2);
hold on;
h2=plot(NO(:,1),NO(:,2),'-.','color',darkred,'linewidth',2);
h3=plot(SW(:,1),SW(:,2),':','color',blue,'linewidth',2);
h4=plot(UK(:,1),UK(:,2),'--','color',purple,'linewidth',2);
h5=plot(US(:,1),US(:,2),'+-','markersize',5,'markerfacecolor',grey,'color',grey,'linewidth',1);

xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:5:100);
set(gca,'xtick',1870:10:2000)
box off;
legend([h1,h2,h3,h4,h5],'Japan','Norway','Sweden','UK','US','location','south')
legend boxoff
xlabel('Cohort');
ylabel('Absolute mobility (%)');

%Export figure
set(gca, 'YGrid', 'on', 'XGrid', 'off')
set(gcf,'color','w');
set(gcf, 'Position', [50 50 500*1.8 400]);
exportgraphics(gcf,'figure4.jpg','Resolution',1200)
exportgraphics(gcf,'figure4.pdf')
exportgraphics(gcf,'figure4.eps')
close all
clear