
## 功能介绍
raw_awb 是一个命令行工具，完成自动白平衡的功能

## 使用方法
### step 1
在环境变量 path 中添加 raw_awb 的路径

### step 2
保存图像到某一个路径，比如 f:\test\8x8_8.raw

### step 3
打开 命令控制台，输入如下信息
raw_awb -f f:\test\8x8_8.raw -i 8 8 -b "RG"
会输出一个计算好白平衡的图像

### step 4
选项信息

-d 打印调试信息

-f 输入文件的路径

-p 像素格式 默认8bit

-i [width height] 输入图像的宽高

-a [offset_x offset_y width height] 感兴趣区域，默认是最大窗口

-b 输入图像的像素格式，包括 "RG" "GR" "BG" "GB" 四种
