rgbimage = imread('ecg.png');
grayimage = rgb2gray(rgbimage); % for non-indexed images
level = graythresh(grayimage); % threshold for converting image to binary, 
binaryimage = im2bw(grayimage, level); 
% extract the individual red, green, and blue color channels.
redchannel = rgbimage(:, :, 1);
greenchannel = rgbimage(:, :, 2);
bluechannel = rgbimage(:, :, 3);
% make the black parts pure red.
redchannel(~binaryimage) = 255;
greenchannel(~binaryimage) = 0;
bluechannel(~binaryimage) = 0;
% now recombine to form the output image.
rgbimageout = cat(3, redchannel, greenchannel, bluechannel);
imshow(rgbimageout);