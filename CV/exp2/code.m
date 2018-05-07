>> img=imread('16_52_01(900).tiff');
gray=rgb2gray(img);
g=im2bw(gray,graythresh(gray));  % 利用Otsu方法进行阈值化处理，初步分离
se=strel('disk',1);  
g=imerode(g,se);imshow(g);  % 对阈值化后的图像腐蚀，增强效果
board=imfill(g,'holes'); % 孔洞填充，把药板上的药片抹去，得到分离后的药板
imshow(board);
g=double(g);
detected=edge(g,'canny'); % 对二值图像进行边缘检测
[H,T,R]=hough(detected);
P=houghpeaks(H,4,'threshold',ceil(0.3*max(H(:))));
lines=houghlines(detected,T,R,P,'FillGap',50,'MinLength',7); % lines为结构数组，长度等于找到的线段数
max_len=0;
for k=1:length(lines)
       xy=[lines(k).point1; lines(k).point2];
       len=norm(lines(k).point1-lines(k).point2);
       Len(k)=len;
       if(len>max_len)
           max_len=len;
           xy_long=xy;
       end
end
[L1 Index1]=max(Len(:));
k=-(lines(Index1).point1(2)-lines(Index1).point2(2)) / (lines(Index1).point1(1)-lines(Index1).point2(1));
% 以上为求直线斜率
angle=atan(k)*180/pi;
rotated=imrotate(img,-angle,'bilinear','crop'); % 对原图进行图像翻转
imshow(rotated);
% 颜色特征的区域分割
color=rgb2ycbcr(rotated);
y=color(:,:,1);cb=color(:,:,2);cr=color(:,:,3);
threshY=graythresh(y);
bwY=im2bw(y,threshY);
threshCB=graythresh(cb);
bwCB=im2bw(cb,threshCB);
final=~(~bwY+~bwCB);
se=strel('disk',6);
final=imclose(final,se);
final=imopen(final,se); % 对处理的图片先进性闭运算再进行开运算
label=bwlabel(~final);  % 标记位置
stats=regionprops(label,'BoundingBox'); % 在旋转后的图像中标记
figure; imshow(rotated); title('旋转后的图像') 
hold on;
for i=1:length(stats)
        if stats(i).BoundingBox(1) > 10
        rectangle('Position',stats(i).BoundingBox,'edgecolor','r','LineWidth',3);
        end
end