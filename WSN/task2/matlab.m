sensor_num = 100; % 传感网中的节点数
M = (1000+1) * (1000+1);  
r = 0;  
flag = zeros(1,M); % 标记grid中的交点是否在某节点的覆盖范围内
% Increasing COMPOW gradually to approximate the minimum  COMPOW (below)  
x = rand(1,sensor_num); 
y = rand(1,sensor_num);
matrix = zeros(sensor_num);
% 生成传感网的邻接矩阵
for R = 0:0.01:1  
    for i=1:1:sensor_num  
        for j = (i+1):1:sensor_num  
            if sqrt((x(i)-x(j))^2+(y(i)-y(j))^2) < R  
                matrix(i,j)=1;  
                matrix(j,i)=1;  
            end  
        end  
    end
  
    S=zeros(sensor_num);  
    % 在sensor_num-1跳内，判断矩阵的连通度
    for m=1:1:sensor_num-1  
        S=S + matrix^m; 
        if all(all(S))==1   
            r=R;  
            break;  
        end  
    end   
    if(r~=0)  
        break;  
    end  
end  
r; %Increasing COMPOW gradually to approximate the minimum  COMPOW (above)  
angle= 0:pi / 50:2*pi;  
for k=1:sensor_num  
    figure(1);  
    plot(r*cos(angle)+x(k),r*sin(angle)+y(k));  
    plot(x(k),y(k),'.');  
    axis([0,1,0,1]);  
    axis equal;  
    hold on;  
    figure(2);  
    plot(r*cos(angle)+x(k),r*sin(angle)+y(k));  
    plot(x(k),y(k),'.');  
    fill(r*cos(angle)+x(k),r*sin(angle)+y(k),'g');  
    axis([0,1,0,1]);  
    axis equal;  
    hold on;  
end 
for i=0:0.001:1  
    for j=0:0.001:1
        for m=1:sensor_num
            if((i-r)<x(m)&&x(m)<(i+r) && (j-r)<y(m)&&y(m)<(j+r))  
                if( (x(m)-i)^2+(y(m)-j)^2 < r*r )  
                    flag(int32(i*1000*1001+j*1000)+1) = 1;  
                    break;  
                end                      
            end  
        end  
    end     
end  

res=sum(flag==1)/M; % 计算总得连通率

