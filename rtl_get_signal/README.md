## 功能介绍
rtl_get_signal 是一个命令行工具，用来解析rtl文件，提取信号名

## 使用须知
目前只支持verilog语法文件，从剪贴板中获取文本数据

## 使用方法
### step 1
将 rtl_get_signal 的路径添加到环境变量 path 中
rtl_get_signal 有1个参数，-d是debug信息

### step 2
复制所选文本，在控制台输入如下信息
rtl_get_signal

### step 3
所选文本信息为
```
	parameter	C_CLKOUT1_DIVIDE	= 1		,	//CLK1分频
	output					clk_out3		,	//pll clkout3
	wire			sys_clk_ibufg		;
	localparam	CLK_PERIOD_NS		= C_INCLK_PERIOD / 1000.0;
	.SIM_DEVICE        		("SPARTAN6"			),
	assign async_rst = sys_rst | ~powerup_pll_locked;
```

控制台会返回如下信息：

```
C_CLKOUT1_DIVIDE
clk_out3
sys_clk_ibufg
CLK_PERIOD_NS
SIM_DEVICE
async_rst
```

## 与UE结合

### step 1
点击菜单中的高级->工具配置，点击插入，新建一个高级工具

### step 2
菜单项名称改为：get signal
命令行为：rtl_get_signal
输出选项卡，修改： a.输出到列表框 b.捕获输出

### step 3
在ue选中文本，然后复制，然后执行工具。可以为工具添加快捷键。

### step 5
输出窗口会输出提取的信号名
将信号名复制到剪贴板中，然后再复制到UE当中