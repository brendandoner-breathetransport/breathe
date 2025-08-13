%Creates Figure C.3 - The copula model effect on absolute mobility. This
%figure uses data from the file 'models.mat'

clear
close all;
load('models.mat')

h11=plot(years_top10share_fr(1:end-30),100*A1,'k','linewidth',2);
hold on;
h12=plot(years_top10share_fr(1:end-30),100*A2,'k--','linewidth',2);
h13=plot(years_top10share_fr(1:end-30),100*A3,'k:','linewidth',2);
h14=plot(years_top10share_fr(1:end-30),100*A4,'k^','linewidth',1,'markersize',4);

h21=plot(years_top10share(1:end-30),100*AA1,'color',[0.5 0.5 0.5],'linewidth',2);
hold on;
h22=plot(years_top10share(1:end-30),100*AA2,'--','color',[0.5 0.5 0.5],'linewidth',2);
h23=plot(years_top10share(1:end-30),100*AA3,':','color',[0.5 0.5 0.5],'linewidth',2);
h24=plot(years_top10share(1:end-30),100*AA4,'^','color',[0.5 0.5 0.5],'linewidth',1,'markersize',4);
box off;

xlabel('Cohort');
ylabel('Absolute mobility (%)');

xlim([1910 1990])

%Export figure
set(gcf, 'Position', [10 10 500 400]);
set(gcf,'color','w');
exportgraphics(gcf,'figureC3.jpg','Resolution',1200)
exportgraphics(gcf,'figureC3.pdf')
exportgraphics(gcf,'figureC3.eps')
close all
clear