%Creates Figure E.4 - a comparison of absolute intergenerational mobility
%estimates in the United States. This script only creates the plot using
%'cps_res.mat'. The absolute mobility estimates plotted are based on a code
%named 'run_cps_age_abs_weights.m', which is included in the 'Other code'
%folder. It could possibly take a few days to run, so to simplify the
%replication the simulation is separated from the plotting script.

clear;
close all;
load('cps_res.mat');

grey=[0.5 0.5 0.5];
purple=[0.494 0.184 0.556];
black=[0 0 0];
blue=[0 0.447 0.741];
darkred=[0.635 0.078 0.184];
green=[0 0.5 0];
cyan=[0.301 0.745 0.933];

close all
subplot(2,2,1:2)
h0=fill([YEARS(1:24)' fliplr(YEARS(1:24)')],[(min([absm01(1:24,[1 2 3 4 6 ]) absm(1:24,[1 2 3 4 6 ]) absm05(1:24,[1 2 3 4 6 ])]')) fliplr(max([absm01(1:24,[1 2 3 4 6 ]) absm(1:24,[1 2 3 4 6 ]) absm05(1:24,[1 2 3 4 6 ])]'))],'k');
set(h0,'facealpha',.12)
set(h0,'linestyle','none')
hold on
h1=plot(usa(usa(:,1)>=1940,1),usa(usa(:,1)>=1940,2),'k','linewidth',3);
h2=plot(usa(usa(:,1)>=1940,1),usa(usa(:,1)>=1940,3),':','color',[0.5 0.5 0.5],'linewidth',3);
h3=plot(YEARS(1:24),absm(1:24,1),'color',[0, 0.4470, 0.7410],'linewidth',2);
h4=plot(YEARS(1:24),absm(1:24,2),'-','color',[0.4940, 0.1840, 0.5560],'linewidth',2);
h5=plot(YEARS(1:24),absm(1:24,3),'-','color',[0.4660, 0.6740, 0.1880],'linewidth',1);
h9=plot(YEARS(1:24),absm(1:24,7),'k+:','linewidth',1);
h6=plot(YEARS(1:24),absm(1:24,4),'-','linewidth',2);
h8=plot(YEARS(1:24),absm(1:24,6),'x-','color',cyan,'linewidth',1);

set(h3,'color',darkred,'linewidth',2,'linestyle','-.')
set(h4,'color',blue,'linestyle',':','linewidth',2);
set(h5,'color',purple,'linestyle','--','linewidth',2);
set(h6,'color',green,'linestyle','-','linewidth',1);

ylim([30 100])
xlim([1940 1985])
xticks([1940:5:1985])
yticks([0:10:100])
xlabel('Cohort');
ylabel('Absolute mobility (%)');
legend([h1,h2,h3,h4,h5,h9,h6,h8],'Baseline','Chetty et al. (2017)','CPS - all adults','CPS - 30 year-olds','CPS - 40 year-olds','CPS - 40 year-olds vs. 30 year-olds','CPS - 35-45 year-olds, family income per adult','CPS - 35-45 year-olds, family income','location','southwest')
legend boxoff
set(gca, 'YGrid', 'on', 'XGrid', 'off')
box off

subplot(2,2,3)
h1=plot(YEARS(1:end-30),moving_average((means(31:end)./means(1:end-30))-1,2)*100,'color',[0, 0.4470, 0.7410],'linewidth',2);
hold on
h2=plot(YEARS(1:end-30),moving_average((means30(31:end)./means30(1:end-30))-1,2)*100,'--','color',[0.4940, 0.1840, 0.5560],'linewidth',2);
h3=plot(YEARS(1:end-30),moving_average((means40(31:end)./means40(1:end-30))-1,2)*100,'-','color',[0.4660, 0.6740, 0.1880],'linewidth',1);
h5=plot(YEARS(1:end-30),moving_average((means40(31:end)./means30(1:end-30))-1,2)*100,'k+:','linewidth',1);
h4=plot(YEARS(1:end-30),moving_average((meansh(31:end)./meansh(1:end-30))-1,2)*100,'x-','color',cyan,'linewidth',1);

ylim([0 71])
xlim([1960 1985])
xticks([1960:5:1985])
yticks([0:5:100])
xlabel('Cohort');
ylabel('30 year growth (%)');
legend([h1,h2,h3,h5,h4],'CPS - all adults','CPS - 30 year-olds','CPS - 40 year-olds','CPS - 40 year-olds vs. 30 year-olds','CPS - 35-45 year-olds, family income','location','southwest')
legend boxoff
set(gca, 'YGrid', 'on', 'XGrid', 'off')
box off
set(h1,'color',darkred,'linewidth',2,'linestyle','-.')
set(h2,'color',blue,'linestyle',':','linewidth',2);
set(h3,'color',purple,'linestyle','--','linewidth',2);

subplot(2,2,4)
h1=plot(YEARS(1:end-30),moving_average((ineqs(31:end)-ineqs(1:end-30)),2),'color',[0, 0.4470, 0.7410],'linewidth',2);
hold on
h2=plot(YEARS(1:end-30),moving_average((ineqs30(31:end)-ineqs30(1:end-30)),2),'--','color',[0.4940, 0.1840, 0.5560],'linewidth',2);
h3=plot(YEARS(1:end-30),moving_average((ineqs40(31:end)-ineqs40(1:end-30)),2),'-','color',[0.4660, 0.6740, 0.1880],'linewidth',1);
h4=plot(YEARS(1:end-30),moving_average((ineqsh(31:end)-ineqsh(1:end-30)),2),'x-','color',cyan,'linewidth',1);

ylim([-6 10])
xlim([1960 1985])
xticks([1960:5:1985])
yticks([-10:2:100])
xlabel('Cohort');
ylabel('Change in top 10% income share (pp)');
legend([h1,h2,h3,h4],'CPS - all adults','CPS - 30 year-olds','CPS - 40 year-olds','CPS - 35-45 year-olds, family income','location','southeast')
legend boxoff
set(gca, 'YGrid', 'on', 'XGrid', 'off')
box off
set(h1,'color',darkred,'linewidth',2,'linestyle','-.')
set(h2,'color',blue,'linestyle',':','linewidth',2);
set(h3,'color',purple,'linestyle','--','linewidth',2);

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*2 400*2]);
exportgraphics(gcf,'figureE4.jpg','Resolution',1200)
exportgraphics(gcf,'figureE4.pdf')
exportgraphics(gcf,'figureE4.eps')
close all
clear