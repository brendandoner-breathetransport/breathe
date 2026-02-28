%Creates Figure C.1 - The effect of the copula resolution on absolute mobility.
%This script only creates the plot using the data in the file
%'decomposition_check.mat'. These results are based on a code named
%'check_copula_vs_analytic.m', which is included in the 'Other code'
%folder. It could possibly take hours to run, so to simplify the
%replication the simulation is separated from the plotting script.

clear
close all
load('decomposition_check.mat')

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];
fs=[10 20 40 50 80 100];
X=0:100;

h1=plot(X,BBBB1(1)*ones(size(X)),'-.','color',black,'linewidth',2);
hold on
h2=plot(fs,BBBB1(3:end),'o-','markersize',5,'markerfacecolor',darkred,'color',darkred,'linewidth',1);

h3=plot(X,BBBB2(1)*ones(size(X)),'-.','color',black,'linewidth',2);
h4=plot(fs,BBBB2(3:end),'s-','markersize',5,'markerfacecolor',blue,'color',blue,'linewidth',1);

h5=plot(X,BBBB3(1)*ones(size(X)),'-.','color',black,'linewidth',2);
h6=plot(fs,BBBB3(3:end),'^-','markersize',5,'markerfacecolor',purple,'color',purple,'linewidth',1);

h7=plot(X,BBBB4(1)*ones(size(X)),'-.','color',black,'linewidth',2);
h8=plot(fs,BBBB4(3:end),'+-','markersize',6,'markerfacecolor',grey,'color',grey,'linewidth',1);

legend([h2,h4,h6,h8],'1950','1960','1970','1980','location','northeast')
legend boxoff

xlim([0 100]);
ylim([50 100]);set(gca,'ytick',50:5:100)
set(gca,'xtick',fs)
box off;
xlabel('Copula resolution (# of fractiles)');
ylabel('Absolute mobility (%)');
grid on

%Export figure
set(gca, 'YGrid', 'on', 'XGrid', 'off')
set(gcf,'color','w');
set(gcf, 'Position', [80 80 500 400]);
exportgraphics(gcf,'figureC1.jpg','Resolution',1200)
exportgraphics(gcf,'figureC1.pdf')
exportgraphics(gcf,'figureC1.eps')
close all
clear