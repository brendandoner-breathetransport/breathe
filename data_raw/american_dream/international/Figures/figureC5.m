%Creates Figure C.5 - The decrease in absolute mobility with changing rank
%correlation. Requires results and data included in 'overturn.mat'

clear;
close all;
load('overturn.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

subplot(1,2,1)

rhos=0:0.01:1;
h1=plot(rhos,AS(2:end),'-k','linewidth',2);hold on;plot(0.22,AS(1),'o','color',black,'markerfacecolor',black,'linewidth',2);
h2=plot(rhos,CA(2:end),'color',darkred,'linewidth',2);hold on;plot(0.27,CA(1),'o','color',darkred,'markerfacecolor',darkred,'linewidth',2);
h3=plot(rhos,DK(2:end),'color',blue,'linewidth',2);hold on;plot(0.19,DK(1),'o','color',blue,'markerfacecolor',blue,'linewidth',2);
h4=plot(rhos,FI(2:end),'color',purple,'linewidth',2);hold on;plot(0.19,FI(1),'o','color',purple,'markerfacecolor',purple,'linewidth',2);
h5=plot(rhos,FR(2:end),'color',grey,'linewidth',2);hold on;plot(0.3,FR(1),'o','color',grey,'markerfacecolor',grey,'linewidth',2);

set(h2,'color',darkred,'linestyle','-.')
set(h3,'color',blue,'linestyle',':')
set(h4,'color',purple,'linestyle','--')
set(h5,'color',grey,'linewidth',1)

ylim([0 60])
xticks([0:0.1:1])
yticks([0:5:100])
legend([h1,h2,h3,h4,h5],'Australia (1950-1986)','Canada (1950-1980)','Denmark (1950-1980)','Finland (1950-1979)','France (1940-1984)','location','northwest')
legend boxoff

ylabel('Overall decrease in abs. mobility (pp)')
xlabel('Rank correlation')
grid on
box off

subplot(1,2,2)

h1=plot(rhos,JP(2:end),'-k','linewidth',2);hold on;plot(0.3,JP(1),'o','color',black,'markerfacecolor',black,'linewidth',2);
h2=plot(rhos,NO(2:end),'color',darkred,'linewidth',2);hold on;plot(0.21,NO(1),'o','color',darkred,'markerfacecolor',darkred,'linewidth',2);
h3=plot(rhos,SW(2:end),'color',blue,'linewidth',2);hold on;plot(0.2,SW(1),'o','color',blue,'markerfacecolor',blue,'linewidth',2);
h4=plot(rhos,UK(2:end),'color',purple,'linewidth',2);hold on;plot(0.3,UK(1),'o','color',purple,'markerfacecolor',purple,'linewidth',2);
h5=plot(rhos,US(2:end),'color',grey,'linewidth',2);hold on;plot(0.3,US(1),'o','color',grey,'markerfacecolor',grey,'linewidth',2);

ylim([0 60])
xticks([0:0.1:1])
yticks([0:5:100])
set(h2,'color',darkred,'linestyle','-.')
set(h3,'color',blue,'linestyle',':')
set(h4,'color',purple,'linestyle','--')
set(h5,'color',grey,'linewidth',1)

legend([h1,h2,h3,h4,h5],'Japan (1947-1980)','Norway (1950-1981)','Sweden (1940-1983)','UK (1959-1984)','US (1940-1980)','location','northwest')
legend boxoff

ylabel('Overall decrease in abs. mobility (pp)')
xlabel('Rank correlation')
grid on
box off

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [100 100 500*2 400]);
exportgraphics(gcf,'figureC5.jpg','Resolution',1200)
exportgraphics(gcf,'figureC5.pdf')
exportgraphics(gcf,'figureC5.eps')
close all
clear