%Creates Figure E.1 - The absolute intergenerational mobility in Denmark,
%Norway and Sweden implementing assortative mating on individual income
%data. This figure uses data on copulas from the data file
%'assortative_check.mat'. It also includes (appended below and commented
%out) a short script that demonstrates how the assortative mating was
%implemented. Also note that the way this is implemented involves random
%matching, so each calculation is slightly different (unless starting from
%the same seed)

clear
close all
load('assortative_check.mat');

subplot(1,3,1)
h4=plot(DK(:,1),DK(:,2),'color','k','linewidth',2);
hold on;
h5=plot(DK(:,1),DK(:,3),'k:','linewidth',2);
h6=plot(DK(:,1),DK(:,4),'ks','linewidth',2);
title('Denmark')
legend('Baseline','Conservative estimate','Realistic estimate','location','southwest')
legend boxoff
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
grid on
xlim([1950 1985])
ylim([60 100])

subplot(1,3,2)
h4=plot(NO(:,1),NO(:,2),'color','k','linewidth',2);
hold on;
h5=plot(NO(:,1),NO(:,3),'k:','linewidth',2);
h6=plot(NO(:,1),NO(:,4),'ks','linewidth',2);
title('Norway')
legend('Baseline','Conservative estimate','Realistic estimate','location','southwest')
legend boxoff
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
grid on
xlim([1950 1985])
ylim([60 100])

subplot(1,3,3)
h4=plot(SW(:,1),SW(:,2),'color','k','linewidth',2);
hold on;
h5=plot(SW(:,1),SW(:,3),'k:','linewidth',2);
h6=plot(SW(:,1),SW(:,4),'ks','linewidth',2);
title('Sweden')
legend('Baseline','Conservative estimate','Realistic estimate','location','southwest')
legend boxoff
box off;
xlabel('Cohort');
ylabel('Absolute mobility (%)');
grid on
xlim([1950 1985])
ylim([60 100])

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*2.7 400]);
exportgraphics(gcf,'figureE1.jpg','Resolution',1200)
exportgraphics(gcf,'figureE1.pdf')
exportgraphics(gcf,'figureE1.eps')
close all
clear

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Implementation of assortative mating
%S1 and S2 are the samples representing the parents and children,
%respectively. NN is the length of these samples.
%
%
% corrspouse1=0.0; %this is set to zero - no assortative mating
% corrspouse2=0.3;
%
%for i=1:nyears
% p1=randperm(NN);
% S1_1=S1(p1(1:NN/2));
% S1_2=S1(p1(NN/2+1:NN));
% [w1,w2]=couple_vecs2(S1_1,S1_2,sin(corrspouse1*pi/6)*2,'gaussian');
% S11=w1+w2;
% p2=randperm(NN);
% S2_1=S2(p2(1:NN/2));
% S2_2=S2(p2(NN/2+1:NN));
% [w1,w2]=couple_vecs2(S2_1,S2_2,sin(corrspouse1*pi/6)*2,'gaussian');
% S22=w1+w2;
% [w1,w2]=couple_vecs2(S11,S22,sin(ctmp*pi/6)*2,'gaussian');
% conservative(i)=absmob0(w1,w2); %this is the actual result for the case
% of no assortative mating
%
% p1=randperm(NN);
% S1_1=S1(p1(1:NN/4));
% S1_2=S1(p1(NN/4+1:NN/2));
% S1_3=S1(p1(NN/2+1:NN));
% [w1,w2]=couple_vecs2(S1_1,S1_2,sin(corrspouse2*pi/6)*2,'gaussian');
% S11=w1+w2;
% S11=[S11; S1_3];
% p2=randperm(NN);
% S2_1=S2(p2(1:NN/4));
% S2_2=S2(p2(NN/4+1:NN/2));
% S2_3=S2(p2(NN/2+1:NN));
% [w1,w2]=couple_vecs2(S2_1,S2_2,sin(corrspouse2*pi/6)*2,'gaussian');
% S22=w1+w2;
% S22=[S22; S2_3];
% [w1,w2]=couple_vecs2(S11,S22,sin(ctmp*pi/6)*2,'gaussian');
% realistic(i)=absmob0(w1,w2); %this is the actual result for the case
% of realistic assortative mating