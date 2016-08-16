function CS(XX,YY,outP,X,Y)


x=length(XX);
y=length(YY);

G=zeros(x,y);
H=G;


for i = 1:x
    for j = 1:y
        A = [XX(i),YY(j)];
        output=mperk('X',X,'Y',Y,'Xpred',A,'UseCorModel',outP);
        G(j,i)=output.preds.se;
        H(j,i)=output.preds.ypreds;
    end
end

save('Coulomb','XX','YY','G','H');

HH = 1.0 ./ H;

figure
surf(XX,YY,HH);
xlabel('\bf \phi_{int}','fontsize',16);
ylabel('\bf \phi_{bed}','fontsize',16);
zlabel('\bf Intersection/Distance');
box on

% figure
% surf(XX,YY,H);
% xlabel('\bf \mu','fontsize',16);
% ylabel('\bf \xi','fontsize',16);
% zlabel('\bf Intersection');
% box on

% figure
% surf(XX,YY,HH);
% xlabel('\bf \mu','fontsize',16);
% ylabel('\bf \xi','fontsize',16);
% zlabel('\bf Distance');
% box on
end
