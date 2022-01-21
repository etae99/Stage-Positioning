Nx = 12;
Ny = 18;
A = zeros(18,12);
Nt = 10;

figure(1); clf;
for i = 1:Ny
    for j = 1:Nx
        disp([num2str(i) '_' num2str(j)]);
        II = [];
        for k = 2:Nt
            M = csvread(['results/' num2str(i-1) '_' num2str(j-1) '_0_Spectrum_' num2str(k-1) '.bmp_spectrum.csv']);
            wavenumber = M(1,:);
            I = M(2,:);
            II = [II;I];
        end
        figure(1);
        II = mean(II,1);
        plot(wavenumber,II); hold on;
        A(i,j) = max(II(:));
    end
end

%%
figure(1);
xlim([200,2000]);
setFigureElements(gcf,gca,'wavenumber (cm^{-1})','I','',20);
saveas(gcf,'spectrum.png');

%%
figure(2);
pcolor(A); shading flat; colorbar; 
axis equal;
axis tight;
saveas(gcf,'max.png');