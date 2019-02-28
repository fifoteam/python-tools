
## 功能介绍
raw_pattern 是一个命令行工具，完成多种测试图的功能

## 使用方法
### step 1
在环境变量 path 中添加 raw_pattern 的路径

### step 2
打开 命令控制台，输入如下信息
raw_pattern -f f:\test\ -i 8 8 -m "random"
在 f:\test\ 目录下生成一个 raw_pattern.raw 的文件，图像分辨率是8x8，像素数据是随机数

### step 5
选项信息

-d 打印调试信息

-o 输出文件的路径

-p 像素格式 默认8bit

-b bayer格式 暂不支持
	"mono"					- 黑白格式
	"rg"					- rg格式
	"gr"					- gr格式
	"bg"					- bg格式
	"gb"					- gb格式

-i [width height] 输出图像宽高

-m [] 测试图的模式，包括以下几种
	"random"                - 随机数

	"pix_inc"               - 第一个像素是0，整帧图像依次递增

	"slide_fix"             - 静态斜条纹，每一行的第一个像素是0，行内依次递增，第二行的第一个像素是1，行内一次递增

	"line_inc"              - 第一行的所有数据都是0，第二行的所有数据都是1，依次循环

	"frame_fix N"           - 整帧灰度为固定值，N的取值范围为0-255

	"walking-0"             - 暂不支持

	"walking-1"             - 暂不支持

	"hammer"                - 暂不支持

	"neighbor"              - 暂不支持

