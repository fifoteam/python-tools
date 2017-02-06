
##功能介绍
raw_sub_bin 是一个命令行工具，完成binning subsample的功能

##使用方法
### step 1
在环境变量 path 中添加 raw_sub_bin 的路径

### step 2
保存图像到某一个路径，比如 f:\test\8x8_8.raw

### step 3
打开 命令控制台，输入如下信息
raw_sub_bin -f f:\test\8x8_8.raw -i 2 2
在同级目录下，会生成一个 8x8_8_sub_2x2.raw的文件，该文件是8x8的图像，默认会做subsample处理，xy方向都会做2倍的缩小

### step 5
选项信息

-d 打印调试信息

-f 输入文件的路径

-p 像素格式 默认8bit

-i [width height] 原始图像宽高

-b 改为binning方式处理图像，默认是subsample

-r [x y xy] x-只做x方向的缩小 y-只做y方向的缩小 xy-xy方向都缩小.默认是xy

-k [2 3 4 ...] 缩小时跳跃的间隔，即skip距离。彩色与黑白的处理方式不一样，彩色的以4个像素为一个基本单位。黑白的以一个像素为基本单位。默认是2，即两个基本单位。

-m 改为mono的方式处理图像，默认是color.该参数只对skip距离起作用.
