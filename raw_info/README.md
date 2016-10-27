
##功能介绍
raw_info 是一个命令行工具，可以从raw图分析出数据信息

##使用方法
### step 1
在环境变量 path 中添加 raw_info 的路径

### step 2
保存图像到某一个路径，比如 f:\test\4912x3684_12.raw

### step 3
打开 命令控制台，输入如下信息
raw_info f:\test\4912x3684_12.raw 12
其中第一个参数是文件的路径 第二个参数12是图像位宽，目前最大支持32bit位宽

### step 4
程序会在控制台中打印出统计信息，也会输出一个4912x3684_12_info.txt的文件

### step 5
文件分析

会分析出像素个数，像素点的最小值、最大值和平均值
```
src file is f:\XHT\zme\script\python\main\raw_info\test\4912x3684_12.raw
pixel_num is 18095808
pixel_min is 301
pixel_max is 4095
pixel_aver is 1183.7217666655172
```
