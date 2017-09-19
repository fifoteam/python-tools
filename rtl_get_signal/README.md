## 功能介绍
rtl_get_signal 是一个命令行工具，用来解析rtl文件，提取信号名

## 使用须知
目前只支持verilog语法文件

## 使用方法
### step 1
将rtl_parser的路径添加到环境变量 path 中
rtl_parser 有两个参数，第一个参数是文件全路径的名字，第二个是所选信号的名字

### step 2
在控制台输入如下信息
rtl_parser -f f:\fpga\src\data_channel\interrupt.v -s fval_fall


### step 3
控制台会返回如下信息：

```
rtl_parser v1.0 2016.09.01
src file is  F:\fpga\src\data_channel\interrupt.v
selected word is  fval_fall
find times : 10
***declaration***
F:\fpga\src\data_channel\interrupt.v(66):wire      fval_fall    ;
***driver***
F:\fpga\src\data_channel\interrupt.v(91):assign fval_fall = (fval_shift[1:0]==2'b10) ? 1'b1 : 1'b0;
***reference***
F:\fpga\src\data_channel\interrupt.v(135):if(fval_fall) begin
```

### step 4
命令行信息
-d 打印调试信息

### step 5
所输出的信息包括三部分，第一部分是信号在那里声明，第二部分是信号在哪里被赋值，第三部分是信号在哪里被引用。
点击相应的信息，会跳转到文件的响应行

## 与UE结合

### step 1
点击菜单中的高级->工具配置，点击插入，新建一个高级工具

### step 2
菜单项名称改为：rtl_parser
命令行为：f:\Michael\script\python\main\rtl_parser\dist\rtl_parser.exe -f %f -s %sel%。根据自己的路径修改
输出选项卡，修改： a.输出到列表框 b.捕获输出

### step 3
命令选项卡，将rtl_parser工具向上移动到最上方，此时系统默认的快捷键是 ctrl+shift+0

### step 4
点击菜单中的高级->配置->键映射
找到AdvancedUserTool1，添加一个自己熟悉的快捷键。我添加的快捷键是 ctrl+d

### step 5
在代码中，选中单词，ctrl+d，即可调用 rtl_parser 工具解析verilog文件。
在output窗口点击，可以跳转到相应的行。
