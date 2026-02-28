%Creates Figure C.4 - The evolution of absolute intergenerational mobility
%in advanced economies. Requires results and data included in
%'mobility_with_err.mat'. This figure also displays the absolute mobility
%estimates included in Table H.1.

clear;
close all;
load('mobility_with_err.mat')

grey1=[0.4 0.4 0.4];
grey2=[0.8 0.8 0.8];
grey3=[0.8 0.8 0.8];
grey4=[0.5 0.5 0.5];

subplot(5,2,1)
hh4=fill([AS(:,1)' fliplr(AS(:,1)')],[AS(:,4)' flipud(AS(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(AS(:,1),AS(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Australia')
disp('Australia:');disp([AS(:,1) round(AS(:,2),1)])

subplot(5,2,2)
hh4=fill([CA(:,1)' fliplr(CA(:,1)')],[CA(:,4)' flipud(CA(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(CA(:,1),CA(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Canada')
disp('Canada:');disp([CA(:,1) round(CA(:,2),1)])

subplot(5,2,3)
hh4=fill([DK(:,1)' fliplr(DK(:,1)')],[DK(:,4)' flipud(DK(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(DK(:,1),DK(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Denmark')
disp('Denmark:');disp([DK(:,1) round(DK(:,2),1)])

subplot(5,2,4)
indind=1:length(FI(:,1));indind(11:13)=[];
hh4=fill([FI(indind,1)' fliplr(FI(indind,1)')],[FI(indind,4)' flipud(FI(indind,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(FI(indind,1),FI(indind,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Finland')
disp('Finland:');disp([FI(indind,1) round(FI(indind,2),1)])

subplot(5,2,5)
hh4=fill([FR(:,1)' fliplr(FR(:,1)')],[FR(:,4)' flipud(FR(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(FR(:,1),FR(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('France')
disp('France:');disp([FR(:,1) round(FR(:,2),1)])

subplot(5,2,6)
hh4=fill([JP(:,1)' fliplr(JP(:,1)')],[JP(:,4)' flipud(JP(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(JP(:,1),JP(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Japan')
disp('Japan:');disp([JP(:,1) round(JP(:,2),1)])

subplot(5,2,7)
hh4=fill([NO(:,1)' fliplr(NO(:,1)')],[NO(:,4)' flipud(NO(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(NO(:,1),NO(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Norway')
disp('Norway:');disp([NO(:,1) round(NO(:,2),1)])

subplot(5,2,8)
hh4=fill([SW(:,1)' fliplr(SW(:,1)')],[SW(:,4)' flipud(SW(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(SW(:,1),SW(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('Sweden')
disp('Sweden:');disp([SW(:,1) round(SW(:,2),1)])

subplot(5,2,9)
hh4=fill([UK(:,1)' fliplr(UK(:,1)')],[UK(:,4)' flipud(UK(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(UK(:,1),UK(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('United Kingdom')
disp('United Kingdom:');disp([UK(:,1) round(UK(:,2),1)])

subplot(5,2,10)
hh4=fill([US(:,1)' fliplr(US(:,1)')],[US(:,4)' flipud(US(:,3))'],'k');
set(hh4,'facealpha',.25)
set(hh4,'linestyle','none')
hold on;
hh00=plot(US(:,1),US(:,2),'k-','linewidth',2);
xlim([1900 1990]);
ylim([50 100]);set(gca,'ytick',50:10:100,'fontsize',8);
set(gca,'xtick',1870:10:2000)
box off;
xlabel('Cohort','fontsize',9);
ylabel('Abs. mobility (%)','fontsize',9);
grid on
title('United States')
disp('United States:');disp([US(:,1) round(US(:,2),1)])

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*1.75 520*1.9]);
exportgraphics(gcf,'figureC4.jpg','Resolution',1200)
exportgraphics(gcf,'figureC4.pdf')
exportgraphics(gcf,'figureC4.eps')
close all
clear