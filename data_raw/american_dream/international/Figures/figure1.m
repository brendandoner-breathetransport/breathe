%Creates Figure 1 - Descriptive scenarios of intergenerational changes in the income distribution
%This code uses no data, it produces an example, thus uses ad-hoc
%parameters

clear
close all

green=[0.466 0.674 0.188];
darkred=[0.635 0.078 0.184];
blue=[0 0.447 0.741];

alpha=0.6;

%Scenario 1
mu1=50;
sig1=8;
X1=mu1-4*sig1:0.1:mu1+4*sig1;
mu2=105;
sig2=8;
X2=mu2-4*sig2:0.1:mu2+4*sig2;
close all;
subplot(1,3,1)
h1=bar(X1,normpdf(X1,mu1,sig1),'hist');
set(h1,'linestyle','none')
set(h1,'facecolor',darkred)
set(h1,'FaceAlpha',alpha);
hold on;
h2=bar(X2,normpdf(X2,mu2,sig2),'hist');
set(h2,'linestyle','none')
set(h2,'facecolor',blue)
set(h2,'FaceAlpha',alpha);
set(gca,'xtick',[])
set(gca,'ytick',[])
box off;
xlabel('Income');
ylabel('Probability density');

%Scenario 2
mu1=50;
sig1=8;
X1=mu1-4*sig1:0.1:mu1+4*sig1;
mu2=65;
sig2=8;
X2=mu2-4*sig2:0.1:mu2+4*sig2;
subplot(1,3,2)
h1=bar(X1,normpdf(X1,mu1,sig1),'hist');
set(h1,'linestyle','none')
set(h1,'facecolor',darkred)
set(h1,'FaceAlpha',alpha);
hold on;
h2=bar(X2,normpdf(X2,mu2,sig2),'hist');
set(h2,'linestyle','none')
set(h2,'facecolor',blue)
set(h2,'FaceAlpha',alpha);
set(gca,'xtick',[])
set(gca,'ytick',[])
box off;
xlabel('Income');
ylabel('Probability density');

%Scenario 3
mu1=50;
sig1=8;
X1=mu1-4*sig1:0.1:mu1+4*sig1;
mu2=105;
sig2=25;
X2=mu2-4*sig2:0.1:mu2+4*sig2;
subplot(1,3,3)
h1=bar(X1,normpdf(X1,mu1,sig1),'hist');
set(h1,'linestyle','none')
set(h1,'facecolor',darkred)
set(h1,'FaceAlpha',alpha);
hold on;
h2=bar(X2,normpdf(X2,mu2,sig2),'hist');
set(h2,'linestyle','none')
set(h2,'facecolor',blue)
set(h2,'FaceAlpha',alpha);
legend([h1,h2],{'Parents','Children'},'location','northeast')
set(gca,'xtick',[])
set(gca,'ytick',[])
legend('boxoff')
box off;
xlabel('Income');
ylabel('Probability density');

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [80 80 500*1.8*3/2 400]);
exportgraphics(gcf,'figure1.jpg','Resolution',1200)
exportgraphics(gcf,'figure1.pdf')
exportgraphics(gcf,'figure1.eps')
close all
clear