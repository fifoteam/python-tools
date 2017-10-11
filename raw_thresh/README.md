
## 功能介绍
raw_thresh 是一个命令行工具，完成 二值化的功能

## 使用方法
### step 1
在环境变量 path 中添加 raw_thresh 的路径

### step 2
保存图像到某一个路径，比如 f:\test\8x8_8.raw

### step 3
打开 命令控制台，输入如下信息
raw_thresh -f f:\test\8x8_8.raw -i 2 2
在同级目录下，会生成一个 8x8_8_mirror_xy.raw的文件，默认会做水平和垂直翻转

### step 5
选项信息

-d 打印调试信息

-f 输入文件的路径

-p 像素格式 默认8bit

-t 阈值，如果不设置，则使用平均值作为阈值
