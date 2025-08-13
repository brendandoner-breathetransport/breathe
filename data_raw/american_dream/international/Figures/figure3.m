%Creates Figure 3 - The sensitivity of absolute mobility to the rank correlation in various simulated scenarios
%This figure requires no input file

clear
close all

rhoo=0:0.01:1;

% Case A: Sharp decrease in inequality
subplot(2,2,1)
h1=plot(gaussian_rhoc(rhoo),100*absmob_logn(10,50,30,rhoo),':k','linewidth',2);
hold on;
h2=plot(gaussian_rhoc(rhoo),100*absmob_logn(50,50,30,rhoo),'color',[0.5 0.5 0.5],'linewidth',2);
h3=plot(gaussian_rhoc(rhoo),100*absmob_logn(100,50,30,rhoo),'-.k','linewidth',2);
h4=plot(gaussian_rhoc(rhoo),100*absmob_logn(400,50,30,rhoo),'--','color',[0, 0.4470, 0.7410],'linewidth',2);
ylim([0 100])
xticks([0:0.1:1])
yticks([0:10:100])
legend([h1,h2,h3,h4],'10% growth','50% growth','100% growth','400% growth','location','southeast','fontsize',10)
legend boxoff
title('A:  Sharp decrease in inequality')
ylabel('Absolute mobility (%)')
xlabel('Rank correlation')
a = annotation('textarrow',[0.2 0.23],[0.78 0.864],'String','Mid-century US');a.FontSize = 10;
grid on
box off

% Case B: No change in inequality
subplot(2,2,2)
h1=plot(gaussian_rhoc(rhoo),100*absmob_logn(10,30,30,rhoo),':k','linewidth',2);
hold on;
h2=plot(gaussian_rhoc(rhoo),100*absmob_logn(50,30,30,rhoo),'color',[0.5 0.5 0.5],'linewidth',2);
h3=plot(gaussian_rhoc(rhoo),100*absmob_logn(100,30,30,rhoo),'-.k','linewidth',2);
h4=plot(gaussian_rhoc(rhoo),100*absmob_logn(400,30,30,rhoo),'--','color',[0, 0.4470, 0.7410],'linewidth',2);
ylim([0 100])
xticks([0:0.1:1])
yticks([0:10:100])
ylabel('Absolute mobility (%)')
xlabel('Rank correlation')
legend([h1,h2,h3,h4],'10% growth','50% growth','100% growth','400% growth','location','southeast','fontsize',10)
legend boxoff
title('B:  No change in inequality')
a = annotation('textarrow',[0.30 0.24],[0.21 0.27],'String','Late 20th century France');a.FontSize = 10;
grid on
box off

% Case C: Mild increase in inequality
subplot(2,2,3)
h1=plot(gaussian_rhoc(rhoo),100*absmob_logn(10,30,35,rhoo),':k','linewidth',2);
hold on;
h2=plot(gaussian_rhoc(rhoo),100*absmob_logn(50,30,35,rhoo),'color',[0.5 0.5 0.5],'linewidth',2);
h3=plot(gaussian_rhoc(rhoo),100*absmob_logn(100,30,35,rhoo),'-.k','linewidth',2);
h4=plot(gaussian_rhoc(rhoo),100*absmob_logn(400,30,35,rhoo),'--','color',[0, 0.4470, 0.7410],'linewidth',2);
ylim([0 100])
xticks([0:0.1:1])
yticks([0:10:100])
legend([h1,h2,h3,h4],'10% growth','50% growth','100% growth','400% growth','location','southwest','fontsize',10)
legend boxoff
title('C:  Mild increase in inequality')
ylabel('Absolute mobility (%)')
xlabel('Rank correlation')
grid on
box off

% Case D: Sharp increase in inequality
subplot(2,2,4)
h1=plot(gaussian_rhoc(rhoo),100*absmob_logn(10,30,45,rhoo),':k','linewidth',2);
hold on;
h2=plot(gaussian_rhoc(rhoo),100*absmob_logn(50,30,45,rhoo),'color',[0.5 0.5 0.5],'linewidth',2);
h3=plot(gaussian_rhoc(rhoo),100*absmob_logn(100,30,45,rhoo),'-.k','linewidth',2);
h4=plot(gaussian_rhoc(rhoo),100*absmob_logn(400,30,45,rhoo),'--','color',[0, 0.4470, 0.7410],'linewidth',2);
ylim([0 100])
xticks([0:0.1:1])
yticks([0:10:100])
legend([h1,h2,h3,h4],'10% growth','50% growth','100% growth','400% growth','location','southwest','fontsize',10)
legend boxoff
title('D:  Sharp increase in inequality')
ylabel('Absolute mobility (%)')
xlabel('Rank correlation')
a = annotation('textarrow',[0.68 0.65],[0.36 0.32],'String','Late 20th century Australia');a.FontSize = 10;
grid on
box off

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 500*2 400*2]);
exportgraphics(gcf,'figure3.jpg','Resolution',1200)
exportgraphics(gcf,'figure3.pdf')
exportgraphics(gcf,'figure3.eps')
close all
clear