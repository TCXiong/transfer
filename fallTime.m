%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Analysis of WF in the case of 1 pulse : calculate the PW, the raise time
% and the fall time (all in ns)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Last update : 27 Sept 2023 by Romain Fons
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all
close all
clc

A = dir('*.csv');

addpath('C:\Users\fonsroma\Documents\FF\ConoscopeProfileProcess')
addpath('C:\Users\fonsroma\Documents\FF\ConoscopeProfileProcess\ResearchToolbox')
% addpath('C:\Users\fonsroma\Documents\Scripts Matlab\Scripts généraux')

Name = 'MZ Jean measurement 1Pulse'; % Used for the title in figure 
Cut_threshold = 1/2; % Cut FWHM (50%) for PW determination
N = 300; % For the smoothdata fonction for not taking into accompt the overshoot, very important to play with this parameter 

for i = 1:length(A)
    Filename = A(i).name;
    
    data = importdata(Filename);
    time = data(:,1)*10^9; % time in ns
    pas_time = time(2)-time(1); %ns/point
    
    intensity = data(:,2); % intensity
    Min_intensity = min(intensity);
    
    % Smooth of the data to remove the "rising" peak for the Max_intensity calculation
    Smooth_intensity = smoothdata(intensity,'gaussian',N);
    
    %     Smooth_intensity = intensity; %Line to avoid the smooth fct in case of too short pulses (sub 0.5ns) or when in the abscence of the overshoot 
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Because of the too low resolution of the measurement, the
    % determination of one cut follow this logic : 
    % 1. find the points right before and right after the real cut (t1, t2)
    % 2. with a linear extrapolation between these two points we find the
    % exact cut position at the exact cut (T1).
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % Calculation of the real PW (ns)
    Max_intensity = max(Smooth_intensity);
    threshold = Max_intensity*Cut_threshold;
    
    % Pulse width
    PW_points = [find(intensity > threshold,1,'first'),find(intensity > threshold,1,'last')];
    t1 = time(PW_points(1)-1);
    t2 = time(PW_points(1));
    Y1 = intensity(PW_points(1)-1);
    Y2 = intensity(PW_points(1));
    T1_PW = (threshold*(t1-t2)-t1*Y2+t2*Y1)/(Y1-Y2);
    
    t3 = time(PW_points(2));
    t4 = time(PW_points(2)+1);
    Y3 = intensity(PW_points(2));
    Y4 = intensity(PW_points(2)+1);
    T2_PW = (threshold*(t3-t4)-t3*Y4+t4*Y3)/(Y3-Y4);
    
    PW_ns(i) = abs(T2_PW-T1_PW);
    
    PW_ns_str = num2str(PW_ns(i),5);
    
    % Raise time 20-80 : cut1=20% - cut2=80%
    cut1 = 0.2;
    cut2 = 0.8;
   
    Raise_points = [find(intensity > Max_intensity*cut1,1,'first'),find(intensity > Max_intensity*cut2,1,'first')];
    t1 = time(Raise_points(1)-1);
    t2 = time(Raise_points(1));
    Y1 = intensity(Raise_points(1)-1);
    Y2 = intensity(Raise_points(1));
    T1_Raise = (Max_intensity*cut1*(t1-t2)-t1*Y2+t2*Y1)/(Y1-Y2);
    
    t3 = time(Raise_points(2)-1);
    t4 = time(Raise_points(2));
    Y3 = intensity(Raise_points(2)-1);
    Y4 = intensity(Raise_points(2));
    T2_Raise = (Max_intensity*cut2*(t3-t4)-t3*Y4+t4*Y3)/(Y3-Y4);
    
    Raise_ns(i) = abs(T2_Raise-T1_Raise);
    
    Raise_ns_str = num2str(Raise_ns(i),5);
    
    % Fall time 20-80
    Fall_points = [find(intensity > Max_intensity*cut2,1,'last'),find(intensity > Max_intensity*cut1,1,'last')];
    t1 = time(Fall_points(1));
    t2 = time(Fall_points(1)+1);
    Y1 = intensity(Fall_points(1));
    Y2 = intensity(Fall_points(1)+1);
    T1_Fall = (Max_intensity*cut2*(t1-t2)-t1*Y2+t2*Y1)/(Y1-Y2);
    
    t3 = time(Fall_points(2));
    t4 = time(Fall_points(2)+1);
    Y3 = intensity(Fall_points(2));
    Y4 = intensity(Fall_points(2)+1);
    T2_Fall = (Max_intensity*cut1*(t3-t4)-t3*Y4+t4*Y3)/(Y3-Y4);
    
    Fall_ns(i) = abs(T2_Fall-T1_Fall);
    
    Fall_ns_str = num2str(Fall_ns(i),5);
 
    % Plot de la figure avec les points des différents cuts
    f = figure;
    plot(time, intensity);
    grid on
    grid minor
    xlim([time(1) time(end)]);
    ylim([Min_intensity-0.005 max(intensity)*1.1]);
    title(Name);
    xlabel('time (ns)');
    ylabel('Intensity (V)');
    hold on
    plot(T1_Raise,Max_intensity*cut1,'b*')
    plot(T2_Raise,Max_intensity*cut2,'b*')
    plot(T1_Fall,Max_intensity*cut2,'r*')
    plot(T2_Fall,Max_intensity*cut1,'r*')
    plot(T1_PW,threshold,'g*')
    plot(T2_PW,threshold,'g*')
    xline(T1_PW,'g')
    xline(T2_PW,'g')
    hold off
    legend(PW_ns_str)
    title(Filename,'Interpreter', 'none');
    
    
    saveas(gcf,[Filename, '_PW_',PW_ns_str,'ns','_Raise_',Raise_ns_str,'ns','_Fall_',Fall_ns_str,'ns','.png'])
    
    
end


PW_ns
Raise_ns
Fall_ns

