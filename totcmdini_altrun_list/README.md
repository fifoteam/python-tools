
## 功能介绍
totcmdini_altrun_list 是一个命令行工具，将total commander的配置文件中的收藏夹转换为altrun list的格式


## 使用方法

wincmd.ini


### step 1
找到total commander的ini文件，比如 f:\test\wincmd.ini

### step 2
打开 命令控制台，输入如下信息
python totcmdini_altrun_list.py -f f:\test\wincmd.ini

### step 3
程序会在 f:\test\ 目录下输出1个解析文件
wincmd_altrunlist.txt

### step 4
关闭altrun
打开wincmd_altrunlist.txt，复制其中的内容，将其copy到altrun的ShortCutList.txt中
打开altrun
就可以用altrun打开total commander的收藏夹

### step 5
命令行信息
-d 打印调试信息
-f 文件路径
