
## 功能介绍
raw_info 是一个命令行工具，可以从raw图分析出数据信息

## 使用方法
### step 1
在环境变量 path 中添加 raw_info 的路径

### step 2
保存图像到某一个路径，比如 f:\test\1280x1024.raw

### step 3
打开 命令控制台，输入如下信息
raw_info -f f:\test\1280x1024.raw
在文件同级目录下面会生成 xxx_info.txt 的文本，内容如下

```
src file is f:\test\1280x1024.raw
pixel_num is 1310720
pixel_min is 20
pixel_max is 108
pixel_aver is 72.52644119262695
```
共有4项内容，像素点个数、像素最小值、像素最大值、像素平均值
上面的命令，是按照8bit位宽分析raw图的


### step 5
在命令行中添加-p参数，可以改变位宽信息
-p [8-32] 指定像素位宽
我们重新存了一张10bit位宽的图像，输入如下命令行
raw_info -f f:\test\1280x1024_10.raw -p 10
得到的信息如下

```
src file is f:\test\1280x1024_10.raw
pixel_num is 1310720
pixel_min is 78
pixel_max is 418
pixel_aver is 284.21031188964844
```

### step 6
高级选项
-d 打印调试信息
-a 打开高级功能
-t [数值] 指定像素阈值

命令行改为：
raw_info -f f:\test\1280x1024.raw -a
在文件同级目录下面会生成 xxx_info.txt 的文本，内容如下

```
src file is f:\test\1280x1024.raw
pixel_num is 1310720
pixel_min is 20
pixel_max is 108
pixel_aver is 72.52644119262695
pixel_max_num is 2
pixel_min_num is 5
pixel_variance is 0.0013797749502510372
pixel_std_dev is 0.037145322050711006
pixel_th_above_num is 1310720
```
增加了几个信息，分别是
pixel_max_num：最大像素点的个数
pixel_min_num：最小像素点的个数
pixel_variance：像素数值方差
pixel_std_dev：像素数值标准差
pixel_th_above_num：在阈值之上的像素点的个数，不包含阈值点，如果没有-t参数，则阈值是0
