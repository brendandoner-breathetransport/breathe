%Creates Figure C.2 - three copulas (transition matrices) constructed by
%composing many delta-local rank-correlation preserving moves. Requires and
%data included in 'copula_moves.mat'

clear
close all
load('copula_moves.mat')

Nfracs=5;

subplot(2,2,1);
mat=aaa2;
imagesc(mat);
colormap(flipud(gray));
textStrings = num2str(mat(:), '%0.2f');
textStrings = strtrim(cellstr(textStrings));
[x, y] = meshgrid(1:Nfracs);
hStrings = text(x(:), y(:), textStrings(:), ...
    'HorizontalAlignment', 'center');
midValue = mean(get(gca, 'CLim'));
textColors = repmat(mat(:) > midValue, 1, 3);
set(hStrings, {'Color'}, num2cell(textColors, 2));
tmptmp=1:Nfracs;
tickss=strsplit(num2str(tmptmp));
set(gca, 'XTick', 1:Nfracs, ...
    'XTickLabel', tickss, ...
    'YTick', 1:Nfracs, ...
    'YTickLabel', tickss, ...
    'TickLength', [0 0]);
xlabel('Quintile of children')
ylabel('Quintile of parents')
title('Copula A')


subplot(2,2,2);
mat=D;
imagesc(mat);
colormap(flipud(gray));
textStrings = num2str(mat(:), '%0.2f');
textStrings = strtrim(cellstr(textStrings));
[x, y] = meshgrid(1:Nfracs);
hStrings = text(x(:), y(:), textStrings(:), ...
    'HorizontalAlignment', 'center');
midValue = mean(get(gca, 'CLim'));
textColors = repmat(mat(:) > midValue, 1, 3);
set(hStrings, {'Color'}, num2cell(textColors, 2));
tmptmp=1:Nfracs;
tickss=strsplit(num2str(tmptmp));
set(gca, 'XTick', 1:Nfracs, ...
    'XTickLabel', tickss, ...
    'YTick', 1:Nfracs, ...
    'YTickLabel', tickss, ...
    'TickLength', [0 0]);
xlabel('Quintile of children')
ylabel('Quintile of parents')
title('Copula B')


subplot(2,2,3);
mat=E;
imagesc(mat);
colormap(flipud(gray));
textStrings = num2str(mat(:), '%0.2f');
textStrings = strtrim(cellstr(textStrings));
[x, y] = meshgrid(1:Nfracs);
hStrings = text(x(:), y(:), textStrings(:), ...
    'HorizontalAlignment', 'center');
midValue = mean(get(gca, 'CLim'));
textColors = repmat(mat(:) > midValue, 1, 3);
set(hStrings, {'Color'}, num2cell(textColors, 2));
tmptmp=1:Nfracs;
tickss=strsplit(num2str(tmptmp));
set(gca, 'XTick', 1:Nfracs, ...
    'XTickLabel', tickss, ...
    'YTick', 1:Nfracs, ...
    'YTickLabel', tickss, ...
    'TickLength', [0 0]);
xlabel('Quintile of children')
ylabel('Quintile of parents')
title('Copula C')


subplot(2,2,4);
h1=plot(years_top10share(1:end-30),baseline,'k','linewidth',2);
hold on
h2=plot(years_top10share(1:end-30),copulaB,'k:','linewidth',2);
h3=plot(years_top10share(1:end-30),copulaC,'-','linewidth',2);

set(h3,'color',[0.5 0.5 0.5])
legend([h1,h2,h3],'Baseline (copula \bf{A})','Copula \bf{B}','Copula \bf{C}','location','southwest')
xlabel('Cohort')
ylabel('Abs. mobility (%)')
legend boxoff
box off
grid on

%Export figure
set(gcf,'color','w');
set(gcf, 'Position', [10 10 400*2 400*2]);
exportgraphics(gcf,'figureC2.jpg','Resolution',1200)
exportgraphics(gcf,'figureC2.pdf')
exportgraphics(gcf,'figureC2.eps')
close all
clear