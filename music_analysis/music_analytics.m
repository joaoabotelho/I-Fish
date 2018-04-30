[y,fs] = wavread(filename); 

y = y(:,1);
dt = 1/fs;
t = 0:dt:(length(y)*dt)-dt;
plot(t,y); xlabel('Seconds'); ylabel('Amplitude');
figure
plot(psd(spectrum.periodogram,y,'Fs',fs,'NFFT',length(y)));
