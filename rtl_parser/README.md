
##���ܽ���
rtl_parser ��һ�������й��ߣ���������rtl�ļ����﷨�����������ԡ�


##ʹ����֪
Ŀǰֻ֧��verilog�﷨�ļ���ֻ�߱��ļ��ڲ���ת�Ĺ��ܡ�

##ʹ�÷���
### step 1
��rtl_parser��·����ӵ��������� path ��
rtl_parser ��������������һ���������ļ�ȫ·�������֣��ڶ�������ѡ�źŵ�����

### step 2
�ڿ���̨����������Ϣ
rtl_parser -f f:\fpga\src\data_channel\interrupt.v -s fval_fall

### step 3
����̨�᷵��������Ϣ��

```
rtl_parser v1.0 2016.09.01
src file is  F:\DAHENG\hw_mer\branches\xinghaotao\u3v\mer-1810-21u3x\fpga\src\data_channel\interrupt.v
selected word is  fval_fall
find times : 10
***declaration***
F:\DAHENG\hw_mer\branches\xinghaotao\u3v\mer-1810-21u3x\fpga\src\data_channel\interrupt.v(66):wire      fval_fall    ;
***driver***
F:\DAHENG\hw_mer\branches\xinghaotao\u3v\mer-1810-21u3x\fpga\src\data_channel\interrupt.v(91):assign fval_fall = (fval_shift[1:0]==2'b10) ? 1'b1 : 1'b0;
***reference***
F:\DAHENG\hw_mer\branches\xinghaotao\u3v\mer-1810-21u3x\fpga\src\data_channel\interrupt.v(135):if(fval_fall) begin
```

### step 4
���������Ϣ���������֣���һ�������ź��������������ڶ��������ź������ﱻ��ֵ�������������ź������ﱻ���á�
�����Ӧ����Ϣ������ת���ļ�����Ӧ��


##��UE���
###step 1
����˵��еĸ߼�->�������ã�������룬�½�һ���߼�����

###step 2
�˵������Ƹ�Ϊ��rtl_parser
������Ϊ��f:\Michael\script\python\main\rtl_parser\dist\rtl_parser.exe -f %f -s %sel%�������Լ���·���޸�
���ѡ����޸ģ� a.������б�� b.�������

###step 3
����ѡ�����rtl_parser���������ƶ������Ϸ�����ʱϵͳĬ�ϵĿ�ݼ��� ctrl+shift+0

###step 4
����˵��еĸ߼�->����->��ӳ��
�ҵ�AdvancedUserTool1�����һ���Լ���Ϥ�Ŀ�ݼ�������ӵĿ�ݼ��� ctrl+d

###step 5
�ڴ����У�ѡ�е��ʣ�ctrl+d�����ɵ��� rtl_parser ���߽���verilog�ļ���
��output���ڵ����������ת����Ӧ���С�
