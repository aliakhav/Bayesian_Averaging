
load('Coulomb.mat')

threshold = 1.75;
N = 512;
n = 0;

for i = 1:N
    for j = 1:N       
        if H(i,j) <= threshold
            n = n + 1;
        end
    end
end

llihood_C = n / N^2;

disp(llihood_C)

% load('Voellmy.mat')
% 
% n = 0;
% 
% for i = 1:N
%     for j = 1:N       
%         if H(i,j) <= threshold
%             n = n + 1;
%         end
%     end
% end
% 
% llihood_V = n / N^2;
% 
% disp(llihood_V)
% 
% load('Pouliquen.mat')
% 
% n = 0;
% 
% for i = 1:N
%     for j = 1:N       
%         if H(i,j) <= threshold
%             n = n + 1;
%         end
%     end
% end
% 
% llihood_P = n / N^2;
% 
% disp(llihood_P)
% 
