## ���ܽ���
rtl_get_signal ��һ�������й��ߣ���������rtl�ļ�����ȡ�ź���

## ʹ����֪
Ŀǰֻ֧��verilog�﷨�ļ����Ӽ������л�ȡ�ı�����

## ʹ�÷���
### step 1
�� rtl_get_signal ��·����ӵ��������� path ��
rtl_get_signal ��1��������-d��debug��Ϣ

### step 2
������ѡ�ı����ڿ���̨����������Ϣ
rtl_get_signal

### step 3
��ѡ�ı���ϢΪ
```
	parameter	C_CLKOUT1_DIVIDE	= 1		,	//CLK1��Ƶ
	output					clk_out3		,	//pll clkout3
	wire			sys_clk_ibufg		;
	localparam	CLK_PERIOD_NS		= C_INCLK_PERIOD / 1000.0;
	.SIM_DEVICE        		("SPARTAN6"			),
	assign async_rst = sys_rst | ~powerup_pll_locked;
```

����̨�᷵��������Ϣ��

```
C_CLKOUT1_DIVIDE
clk_out3
sys_clk_ibufg
CLK_PERIOD_NS
SIM_DEVICE
async_rst
```

## ��UE���

### step 1
����˵��еĸ߼�->�������ã�������룬�½�һ���߼�����

### step 2
�˵������Ƹ�Ϊ��get signal
������Ϊ��rtl_get_signal
���ѡ����޸ģ� a.������б�� b.�������

### step 3
��ueѡ���ı���Ȼ���ƣ�Ȼ��ִ�й��ߡ�����Ϊ������ӿ�ݼ���

### step 5
������ڻ������ȡ���ź���
���ź������Ƶ��������У�Ȼ���ٸ��Ƶ�UE����