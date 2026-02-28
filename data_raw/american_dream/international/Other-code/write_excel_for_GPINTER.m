% This script reads data downloaded from WID using the R script
% 'import_WID_for_GPINTER.R' and exported to the file 'WID_data.csv'
% It converts this file into an xlsx file in a format that can be read by
% the GPINTER online interface
% Please note the output xlsx filename has to be new, it cannot overwrite
% an existing file with the same name

clear

A=importdata('WID_data.csv');
data=A.data;

%xlsx filename
filename = 'WID_input_for_GPINTER.xlsx';

years=unique(data(:,1));
N=length(years);
len=length(data(:,1));
value=data(:,2);

%ps should include all the ranks p
%ps2 should include the same values as ps but in the order they appear in
%the csv file
ps=[0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.95 0.99 0.999 0.9999 0.99999];
ps2=[0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.95 0.99999 0.9999  0.999 0.99];

Np=length(ps);
thres=zeros(N,Np+1);
ave=zeros(N,Np+1);
count=1;
for j=1:Np+1
    for i=1:N
        ave(i,j)=value(count);
        thres(i,j)=value(count+len/2);
        count=count+1;
    end
end
thres(:,1)=[]; thres2=zeros(N,Np); thres2=thres(:,[1 2 3 4 5 6 7 8 9 10 14 13 12 11]);
ave(:,1)=[]; ave2=zeros(N,Np); ave2=ave(:,[1 2 3 4 5 6 7 8 9 10 14 13 12 11]);

ave_total=value(1:N);
for i=1:N
    A = {'year','average'; years(i),ave_total(i)};
    sheet = i;
    xlRange = 'A1';
    xlswrite(filename,A,sheet,xlRange)
    B=cell(Np+1,3);
    B(1,:)={'p','thr','topavg'};
    for j=1:Np
        B(j+1,:)={ps(j),thres2(i,j),ave2(i,j)};
    end
    xlRange = 'C1';
    xlswrite(filename,B,sheet,xlRange)
end