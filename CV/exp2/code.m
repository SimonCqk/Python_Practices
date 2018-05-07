>> img=imread('16_52_01(900).tiff');
gray=rgb2gray(img);
g=im2bw(gray,graythresh(gray));  % ����Otsu����������ֵ��������������
se=strel('disk',1);  
g=imerode(g,se);imshow(g);  % ����ֵ�����ͼ��ʴ����ǿЧ��
board=imfill(g,'holes'); % �׶���䣬��ҩ���ϵ�ҩƬĨȥ���õ�������ҩ��
imshow(board);
g=double(g);
detected=edge(g,'canny'); % �Զ�ֵͼ����б�Ե���
[H,T,R]=hough(detected);
P=houghpeaks(H,4,'threshold',ceil(0.3*max(H(:))));
lines=houghlines(detected,T,R,P,'FillGap',50,'MinLength',7); % linesΪ�ṹ���飬���ȵ����ҵ����߶���
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
% ����Ϊ��ֱ��б��
angle=atan(k)*180/pi;
rotated=imrotate(img,-angle,'bilinear','crop'); % ��ԭͼ����ͼ��ת
imshow(rotated);
% ��ɫ����������ָ�
color=rgb2ycbcr(rotated);
y=color(:,:,1);cb=color(:,:,2);cr=color(:,:,3);
threshY=graythresh(y);
bwY=im2bw(y,threshY);
threshCB=graythresh(cb);
bwCB=im2bw(cb,threshCB);
final=~(~bwY+~bwCB);
se=strel('disk',6);
final=imclose(final,se);
final=imopen(final,se); % �Դ����ͼƬ�Ƚ��Ա������ٽ��п�����
label=bwlabel(~final);  % ���λ��
stats=regionprops(label,'BoundingBox'); % ����ת���ͼ���б��
figure; imshow(rotated); title('��ת���ͼ��') 
hold on;
for i=1:length(stats)
        if stats(i).BoundingBox(1) > 10
        rectangle('Position',stats(i).BoundingBox,'edgecolor','r','LineWidth',3);
        end
end