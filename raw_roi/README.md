
##功能介绍
raw_roi 是一个命令行工具，完成roi图像裁剪的功能

##使用方法
### step 1
在环境变量 path 中添加 raw_info 的路径

### step 2
保存图像到某一个路径，比如 f:\test\2x2_8.raw

### step 3
打开 命令控制台，输入如下信息
raw_roi -f f:\test\2x2_8.raw -i 2 2 -r 0 0 1 1
在同级目录下，会生成一个 2x2_8_0_0_1_1.raw的文件，该文件是2x2的图像裁剪为1x1的图像，起始点是(0,0)

### step 5
选项信息

-d 打印调试信息

-f 输入文件的路径

-p 像素格式 默认8bit

-i [width height] 原始图像宽高

-r [offset_x offset_y roi_width roi_height] roi的起始点和宽高
