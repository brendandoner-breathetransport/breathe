%Creates Figure G.1 - a comparison between the baseline absolute mobility
%estimates with other empirical evidence in different countries. This
%script creates the plot using 'mobility_comparison.mat'.

clear;
close all;
load('mobility_comparison.mat')

grey1=[0.4 0.4 0.4];
grey2=[0.8 0.8 0.8];
grey3=[0.8 0.8 0.8];
grey4=[0.5 0.5 0.5];

subplot(4,2,1)

hh00=plot(canada(:,1),canada(:,2),'k-','linewidth',2);
hold on;
hh11=plot(canada(:,1),canada(:,3),'k:','color',grey4,'linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Canada')

subplot(4,2,2)

hh00=plot(denmark(:,1),denmark(:,2),'k-','linewidth',2);
hold on;
hh11=plot(denmark(:,1),denmark(:,3),'k:','color',grey4,'linewidth',2);
hh22=plot(denmark(:,1),100*denmark(:,4),'k:','color','b','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Denmark')

subplot(4,2,3)
ind1=find(~isnan(finland(:,2)));
ind2=find(~isnan(finland(:,3)));
hh00=plot(finland(ind1,1),finland(ind1,2),'k-','linewidth',2);
hold on;
hh11=plot(finland(ind2,1),finland(ind2,3),'k:','color',grey4,'linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Finland')

subplot(4,2,4)

hh00=plot(norway(:,1),norway(:,2),'k-','linewidth',2);
hold on;
hh11=plot(norway(:,1),norway(:,3),'k:','color',grey4,'linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Norway')

subplot(4,2,5)

hh00=plot(sweden(:,1),sweden(:,2),'k-','linewidth',2);
hold on;
hh11=plot(sweden(:,1),sweden(:,3),'k:','color',grey4,'linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Sweden')

subplot(4,2,6)

hh00=plot(uk(:,1),uk(:,2),'k-','linewidth',2);
hold on;
hh11=plot(uk(:,1),uk(:,3),'k:','color',grey4,'linewidth',2);
hh22=plot(uk(:,1),100*uk(:,4),'k:','color','b','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('United Kingdom')

subplot(4,2,7)

hh00=plot(usa(:,1),usa(:,2),'k-','linewidth',2);
hold on;
hh11=plot(usa(:,1),usa(:,3),'k:','color',grey4,'linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('United States')

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*1.7 400*2.3]);
exportgraphics(gcf,'figureG1.jpg','Resolution',1200)
exportgraphics(gcf,'figureG1.pdf')
exportgraphics(gcf,'figureG1.eps')
close all
clear