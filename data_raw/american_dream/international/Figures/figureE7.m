%Creates Figure E.7 - the decrease in absolute mobility with mis-estimation
%of inequality changes and income growth. This script creates the plot
%using 'tweaks_res.mat'.

clear;
close all;
load('tweaks_res.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];

i_tweaks=(-10:0.1:10)/100;
N=length(i_tweaks)+1;

subplot(2,2,1)
h1=plot(i_tweaks*100,AS1(2:end),'-k','linewidth',2);hold on;plot(0,AS1(1),'o','color','k','markerfacecolor','k','linewidth',2);
h2=plot(i_tweaks*100,CA1(2:end),'-k','linewidth',2);plot(0,CA1(1),'o','color',darkred,'markerfacecolor',darkred,'linewidth',2);
h3=plot(i_tweaks*100,DK1(2:end),'-k','linewidth',2);plot(0,DK1(1),'o','color',blue,'markerfacecolor',blue,'linewidth',2);
h4=plot(i_tweaks*100,FI1(2:end),'-k','linewidth',2);plot(0,FI1(1),'o','color',purple,'markerfacecolor',purple,'linewidth',2);
h5=plot(i_tweaks*100,FR1(2:end),'-k','linewidth',2);plot(0,FR1(1),'o','color',grey,'markerfacecolor',grey,'linewidth',2);

set(h2,'color',darkred,'linestyle','-.')
set(h3,'color',blue,'linestyle',':')
set(h4,'color',purple,'linestyle','--')
set(h5,'color',grey,'linewidth',1)
ylim([0 60])
yticks([0:5:100])
legend([h1,h2,h3,h4,h5],'Australia (1950-1986)','Canada (1950-1980)','Denmark (1950-1980)','Finland (1950-1979)','France (1940-1984)','location','northeast')
legend boxoff
ylabel('Overall decrease in abs. mobility (pp)')
xlabel('Inequality growth underestimation (%)')
grid on
box off

subplot(2,2,2)
h1=plot(i_tweaks*100,JP1(2:end),'-k','linewidth',2);hold on;plot(0,JP1(1),'o','color','k','markerfacecolor','k','linewidth',2);
h2=plot(i_tweaks*100,NO1(2:end),'-k','linewidth',2);plot(0,NO1(1),'o','color',darkred,'markerfacecolor',darkred,'linewidth',2);
h3=plot(i_tweaks*100,SW1(2:end),'-k','linewidth',2);plot(0,SW1(1),'o','color',blue,'markerfacecolor',blue,'linewidth',2);
h4=plot(i_tweaks*100,UK1(2:end),'-k','linewidth',2);plot(0,UK1(1),'o','color',purple,'markerfacecolor',purple,'linewidth',2);
h5=plot(i_tweaks*100,US1(2:end),'-k','linewidth',2);plot(0,US1(1),'o','color',grey,'markerfacecolor',grey,'linewidth',2);

set(h2,'color',darkred,'linestyle','-.')
set(h3,'color',blue,'linestyle',':')
set(h4,'color',purple,'linestyle','--')
set(h5,'color',grey,'linewidth',1)
ylim([0 60])
yticks([0:5:100])
legend([h1,h2,h3,h4,h5],'Japan (1947-1980)','Norway (1950-1981)','Sweden (1940-1983)','UK (1959-1984)','US (1940-1980)','location','northwest')
legend boxoff
ylabel('Overall decrease in abs. mobility (pp)')
xlabel('Inequality growth underestimation (%)')
grid on
box off

g_tweaks=(-10:0.1:10)/100;
N=length(g_tweaks)+1;

subplot(2,2,3)
h1=plot(g_tweaks*100,AS2(2:end),'-k','linewidth',2);hold on;plot(0,AS2(1),'o','color','k','markerfacecolor','k','linewidth',2);
h2=plot(g_tweaks*100,CA2(2:end),'-k','linewidth',2);plot(0,CA2(1),'o','color',darkred,'markerfacecolor',darkred,'linewidth',2);
h3=plot(g_tweaks*100,DK2(2:end),'-k','linewidth',2);plot(0,DK2(1),'o','color',blue,'markerfacecolor',blue,'linewidth',2);
h4=plot(g_tweaks*100,FI2(2:end),'-k','linewidth',2);plot(0,FI2(1),'o','color',purple,'markerfacecolor',purple,'linewidth',2);
h5=plot(g_tweaks*100,FR2(2:end),'-k','linewidth',2);plot(0,FR2(1),'o','color',grey,'markerfacecolor',grey,'linewidth',2);

set(h2,'color',darkred,'linestyle','-.')
set(h3,'color',blue,'linestyle',':')
set(h4,'color',purple,'linestyle','--')
set(h5,'color',grey,'linewidth',1)
ylim([0 60])
yticks([0:5:100])
legend([h1,h2,h3,h4,h5],'Australia (1950-1986)','Canada (1950-1980)','Denmark (1950-1980)','Finland (1950-1979)','France (1940-1984)','location','northeast')
legend boxoff
ylabel('Overall decrease in abs. mobility (pp)')
xlabel('Growth underestimation (%)')
grid on
box off

subplot(2,2,4)
h1=plot(g_tweaks*100,JP2(2:end),'-k','linewidth',2);hold on;plot(0,JP2(1),'o','color','k','markerfacecolor','k','linewidth',2);
h2=plot(g_tweaks*100,NO2(2:end),'-k','linewidth',2);plot(0,NO2(1),'o','color',darkred,'markerfacecolor',darkred,'linewidth',2);
h3=plot(g_tweaks*100,SW2(2:end),'-k','linewidth',2);plot(0,SW2(1),'o','color',blue,'markerfacecolor',blue,'linewidth',2);
h4=plot(g_tweaks*100,UK2(2:end),'-k','linewidth',2);plot(0,UK2(1),'o','color',purple,'markerfacecolor',purple,'linewidth',2);
h5=plot(g_tweaks*100,US2(2:end),'-k','linewidth',2);plot(0,US2(1),'o','color',grey,'markerfacecolor',grey,'linewidth',2);

ylim([0 60])
yticks([0:5:100])
legend([h1,h2,h3,h4,h5],'Japan (1947-1980)','Norway (1950-1981)','Sweden (1940-1983)','UK (1959-1984)','US (1940-1980)','location','northeast')
legend boxoff
ylabel('Overall decrease in abs. mobility (pp)')
xlabel('Growth underestimation (%)')
grid on
box off
set(h2,'color',darkred,'linestyle','-.')
set(h3,'color',blue,'linestyle',':')
set(h4,'color',purple,'linestyle','--')
set(h5,'color',grey,'linewidth',1)

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*2 400*2]);
exportgraphics(gcf,'figureE7.jpg','Resolution',1200)
exportgraphics(gcf,'figureE7.pdf')
exportgraphics(gcf,'figureE7.eps')
close all
clear