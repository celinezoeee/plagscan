

rgbImageIn = imread('ecoli.png');
grayImage = rgb2gray(rgbImageIn);
 
level = graythresh(grayImage); 
binaryImage = im2bw(grayImage, level); 
rChannel = rgbImage(:, :, 1);
gChannel   = rgbImage(:, :, 2);


bChannel = rgbImage(:, :, 3);
rChannel(~binaryImage) = 255;
gChannel(~binaryImage) = 0;
bChannel(~binaryImage) = 0;
rgbImageOut = cat(3, rChannel, gChannel, bChannel);
imshow(rgbImageOut);
     

