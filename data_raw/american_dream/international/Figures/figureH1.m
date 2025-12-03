%Creates Figure H.1 - counterfactual calculations of absolute mobility in a
%group of advanced economies. This script creates the plot using
%'counterfactuals.mat'. This script also produces the results presented in
%Table H.2 using the same data and the same calculation.

clear;
close all;
load('counterfactuals.mat')

subplot(5,2,1)
hh1=plot(AS(:,1),100*AS(:,2)/AS(1,2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(AS(:,1),100*AS(:,3)/AS(1,3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(AS(:,1),100*AS(:,4)/AS(1,4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest');
xlim([1940 1985]);ylim([50 110]);set(gca,'xtick',1900:10:2000);set(gca,'ytick',0:10:200,'fontsize',8)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('Australia')
disp('Australia:');disp(round(mobility_decompose(AS),1));

subplot(5,2,2)
hh1=plot(CA(:,1),100*CA(:,2)/CA(1,2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(CA(:,1),100*CA(:,3)/CA(1,3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(CA(:,1),100*CA(:,4)/CA(1,4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest');
xlim([1940 1985]);ylim([50 110]);set(gca,'xtick',1900:10:2000);set(gca,'ytick',0:10:200,'fontsize',8)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('Canada')
disp('Canada:');disp(round(mobility_decompose(CA),1));

subplot(5,2,3)
hh1=plot(DK(:,1),100*DK(:,2)/DK(1,2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(DK(:,1),100*DK(:,3)/DK(1,3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(DK(:,1),100*DK(:,4)/DK(1,4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest');
xlim([1940 1985]);ylim([50 110]);set(gca,'xtick',1900:10:2000);set(gca,'ytick',0:10:200,'fontsize',8)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('Denmark')
disp('Denmark:');disp(round(mobility_decompose(DK),1));

subplot(5,2,4)
indind=find(~isnan(FI(:,2)));
hh1=plot(FI(indind,1),100*FI(indind,2)/FI(1,2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(FI(indind,1),100*FI(indind,3)/FI(1,3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(FI(indind,1),100*FI(indind,4)/FI(1,4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest');
xlim([1940 1985]);ylim([50 110]);set(gca,'xtick',1900:10:2000);set(gca,'ytick',0:10:200,'fontsize',8)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('Finland')
disp('Finland:');disp(round(mobility_decompose(FI),1));

subplot(5,2,5)
hh1=plot(FR(:,1),100*FR(:,2)/FR(find(FR(:,1)==1940),2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(FR(:,1),100*FR(:,3)/FR(find(FR(:,1)==1940),3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(FR(:,1),100*FR(:,4)/FR(find(FR(:,1)==1940),4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest')
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200,'fontsize',8)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('France')
indind=find(FR(:,1)>=1940);disp('France:');disp(round(mobility_decompose(FR(indind,:)),1));

subplot(5,2,6)
hh1=plot(JP(:,1),100*JP(:,2)/JP(find(JP(:,1)==1947),2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(JP(:,1),100*JP(:,3)/JP(find(JP(:,1)==1947),3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(JP(:,1),100*JP(:,4)/JP(find(JP(:,1)==1947),4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest')
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200,'fontsize',8)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('Japan')
indind=find(JP(:,1)>=1947);disp('Japan:');disp(round(mobility_decompose(JP(indind,:)),1));

subplot(5,2,7)
hh1=plot(NO(:,1),100*NO(:,2)/NO(1,2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(NO(:,1),100*NO(:,3)/NO(1,3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(NO(:,1),100*NO(:,4)/NO(1,4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest');
xlim([1940 1985]);ylim([50 110]);set(gca,'xtick',1900:10:2000);set(gca,'ytick',0:10:200,'fontsize',8)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('Norway')
disp('Norway:');disp(round(mobility_decompose(NO),1));

subplot(5,2,8)
hh1=plot(SW(:,1),100*SW(:,2)/SW(find(SW(:,1)==1940),2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(SW(:,1),100*SW(:,3)/SW(find(SW(:,1)==1940),3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(SW(:,1),100*SW(:,4)/SW(find(SW(:,1)==1940),4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest')
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200,'fontsize',8)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('Sweden')
indind=find(SW(:,1)>=1940);disp('Sweden:');disp(round(mobility_decompose(SW(indind,:)),1));

subplot(5,2,9)
hh1=plot(UK(:,1),100*UK(:,2)/UK(1,2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(UK(:,1),100*UK(:,3)/UK(1,3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(UK(:,1),100*UK(:,4)/UK(1,4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest');
xlim([1940 1985]);ylim([50 110]);set(gca,'xtick',1900:10:2000);set(gca,'ytick',0:10:200,'fontsize',8)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('United Kingdom')
disp('United Kingdom:');disp(round(mobility_decompose(UK),1));

subplot(5,2,10)
hh1=plot(US(:,1),100*US(:,2)/US(find(US(:,1)==1940),2),'-','color','k','linewidth',3);
hold on;grid on
hh2=plot(US(:,1),100*US(:,3)/US(find(US(:,1)==1940),3),'-','color',[0.6 0.6 0.6],'linewidth',3);
hh3=plot(US(:,1),100*US(:,4)/US(find(US(:,1)==1940),4),'-','color',[0.2 0.3 0.7],'linewidth',3);
legend([hh1,hh2,hh3],'Baseline','Fixed inequality','Fixed income growth','Location','southwest')
xlim([1940 1985]);
ylim([50 110]);
set(gca,'ytick',0:10:200,'fontsize',8)
set(gca,'xtick',1900:10:2000)
box off;
xlabel('Cohort','fontsize',8);
ylabel('Abs. mobility, first cohort = 100%','fontsize',8);
legend boxoff
title('United States')
indind=find(US(:,1)>=1940);disp('United States:');disp(round(mobility_decompose(US(indind,:)),1));

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*1.75 520*1.9]);
exportgraphics(gcf,'figureH1.jpg','Resolution',1200)
exportgraphics(gcf,'figureH1.pdf')
exportgraphics(gcf,'figureH1.eps')
close all
clear