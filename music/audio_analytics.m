% filename = 'voice1_music.wav';
file = './voice-beatit';
filename = strcat(file,'.wav');
[data,Fs] = audioread(filename);
inf = audioinfo(filename);

%fileID = fopen('values_audio.txt','r');

%data = fscanf(fileID,"%f");


%fclose(fileID);

data = data(:,1);


length_data = length(data);
x = (0:length_data-1)';
time_per_value = inf.Duration / length_data;

[pks, indexes] = findpeaks(data,x,'MinPeakDistance',1400);
t_values = data(indexes);

diff_indexes = diff(indexes);
array_of_time = diff_indexes * time_per_value ;
% normalized = t_values/norm(t_values)
%normalized(normalized < 0) = 0
normalized = (t_values - min(t_values)) / (max(t_values) - min(t_values));

figure(1)
subplot(2,1,1)
plot(normalized)
subplot(2,1,2)
plot(data)


dlmwrite(file + "-normalized.txt",normalized);
dlmwrite(file + "-array_of_time.txt",array_of_time);


