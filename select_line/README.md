
## ���ܽ���
select_line ��һ�������й��ߣ�������ȡ����־�ļ��а���ĳЩ�����Ҳ�������һЩ������С�

## ʹ����֪
select_line �����з����ı������ƥ��ɹ��������¸��е���Ϣ��
�����������ı�֮�󣬻Ὣ�����Ľ��д�뵽 ����ı����С�

## ʹ�÷���
### step 1
�ڻ������� path ����� select_line ��·��

### step 2
������־��ĳһ��·�������� f:\test\1.txt

### step 3
�� �������̨������������Ϣ
select_line -f f:\test\1.txt -s line -e block

һ���а��� line �Ҳ����� block ���лᱻɸѡ����
1.-f �Ǳ�ѡ�������������ļ�·��

2.-s �ǿ�ѡ����������Ĳ��������ж��������֮���ǡ��򡱵Ĺ�ϵ����ֻҪ��һ�����ʳ��֣���һ�оͻᱻɸѡ������

3.-e �ǿ�ѡ����������Ĳ��������ж��������֮���ǡ��򡱵Ĺ�ϵ����ֻҪ��һ�����ʳ��֣���һ�оͻᱻ�޳���

4.-d �ǿ�ѡ���������ӡ��������Ϣ��

### step 4
������� f:\test\ Ŀ¼�����1�������ļ�
1_select_line.txt

### step 5
�ļ�����

*** 1.txt ***
��־�а���������Ϣ
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

*** select_line.txt ***
����֮����ı�

```
line num is 45	Read ExposureAuto 0x0004Byte
line num is 47	ReadAck 0x00000000
line num is 48	Read ExposureAuto 0x0004Byte
line num is 50	ReadAck 0x00000000
line num is 51	Write ExposureTime 0x000075f6
line num is 53	WriteAck 0x0004Byte
```

