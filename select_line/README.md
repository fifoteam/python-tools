
##功能介绍
select_line 是一个命令行工具，可以提取出日志文件中包含某些词语且不包含另一些词语的行。

##使用须知
select_line 会逐行分析文本，如果匹配成功，则保留下该行的信息。
分析完整个文本之后，会将解析的结果写入到 输出文本当中。

##使用方法
### step 1
在环境变量 path 中添加 select_line 的路径

### step 2
保存日志到某一个路径，比如 f:\test\1.txt

### step 3
打开 命令控制台，输入如下信息
select_line -f f:\test\1.txt -s line -e block

一行中包含 line 且不包含 block 的行会被筛选出来
1.-f 是必选参数，后面是文件路径

2.-s 是可选参数，后面的参数可以有多个。参数之间是“或”的关系，即只要有一个单词出现，这一行就会被筛选出来。

3.-e 是可选参数，后面的参数可以有多个。参数之间是“或”的关系，即只要有一个单词出现，这一行就会被剔除。

4.-d 是可选参数，会打印出调试信息。

### step 4
程序会在 f:\test\ 目录下输出1个解析文件
1_select_line.txt

### step 5
文件分析

***1.txt***
日志中包含如下信息
```
line num is 21	 block is 0x1cfc. chunk_mode_active is 1. timestamp is 0x10c68de0775c. pixel_format is 0x01080008(BayerGR8). size_x is 0x1200(4608). size_y is 0x0cd8(3288). offset_x is 0x0000(0). offset_y is 0x0000(0).
line num is 45	Read ExposureAuto 0x0004Byte
line num is 47	ReadAck 0x00000000
line num is 48	Read ExposureAuto 0x0004Byte
line num is 50	ReadAck 0x00000000
line num is 51	Write ExposureTime 0x000075f6
line num is 53	WriteAck 0x0004Byte
line num is 361	 trailer_size is 36. block is 0x1d02. status is 0x0000. valid_payload_size is 0x00e73028(15151144). trailer_size_y is 0x0cd8(3288). chunk_layout_id is 0x09(9).
line num is 364	 block is 0x1d03. chunk_mode_active is 1. timestamp is 0x10c6bc46c862. pixel_format is 0x01080008(BayerGR8). size_x is 0x1200(4608). size_y is 0x0cd8(3288). offset_x is 0x0000(0). offset_y is 0x0000(0).
line num is 399	 trailer_size is 36. block is 0x1d03. status is 0x0000. valid_payload_size is 0x00e73028(15151144). trailer_size_y is 0x0cd8(3288). chunk_layout_id is 0x09(9).
line num is 402	 block is 0x1d04. chunk_mode_active is 1. timestamp is 0x10c6c2dcdce8. pixel_format is 0x01080008(BayerGR8). size_x is 0x1200(4608). size_y is 0x0cd8(3288). offset_x is 0x0000(0). offset_y is 0x0000(0).
```

***select_line.txt***
解析之后的文本

```
line num is 45	Read ExposureAuto 0x0004Byte
line num is 47	ReadAck 0x00000000
line num is 48	Read ExposureAuto 0x0004Byte
line num is 50	ReadAck 0x00000000
line num is 51	Write ExposureTime 0x000075f6
line num is 53	WriteAck 0x0004Byte
```

