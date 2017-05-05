
## 功能介绍
raw_get_thresh 是一个命令行工具，完成otsu算法提取阈值的功能

## 使用方法
### step 1
在环境变量 path 中添加 raw_get_thresh 的路径

### step 2
保存图像到某一个路径，比如 f:\test\8x8_8.raw

### step 3
打开 命令控制台，输入如下信息
raw_get_thresh -f f:\test\8x8_8.raw
会输出一个otsu算法算出的阈值

### step 5
选项信息

-d 打印调试信息

-f 输入文件的路径

-p 像素格式 默认8bit
