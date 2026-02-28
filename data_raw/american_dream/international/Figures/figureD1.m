%Creates Figure D1 - representations of intergenerational copulas for
% Denmark the United States. This figure uses data on copulas taken from
% the data file 'copulas.mat' It simply plots two 5x5 matrices.

clear
close all;
load('copulas.mat')

Nfracs=5;
mat=dk4;
subplot(1,2,1);

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
title('Denmark (Jäntti et al. (2006))')

mat=copula5_USA_eberharter;
subplot(1,2,2);

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
title('United States (Eberharter (2014))')

%Export figure
set(gcf, 'Position', [10 10 500*1.8 400]);
set(gcf,'color','w');
exportgraphics(gcf,'figureD1.jpg','Resolution',1200)
exportgraphics(gcf,'figureD1.pdf')
exportgraphics(gcf,'figureD1.eps')
close all
clear