
##���ܽ���
raw_info ��һ�������й��ߣ����Դ�rawͼ������������Ϣ

##ʹ�÷���
### step 1
�ڻ������� path ����� raw_info ��·��

### step 2
����ͼ��ĳһ��·�������� f:\test\1280x1024.raw

### step 3
�� �������̨������������Ϣ
raw_info -f f:\test\1280x1024.raw
���ļ�ͬ��Ŀ¼��������� xxx_info.txt ���ı�����������

```
src file is f:\test\1280x1024.raw
pixel_num is 1310720
pixel_min is 20
pixel_max is 108
pixel_aver is 72.52644119262695
```
����4�����ݣ����ص������������Сֵ���������ֵ������ƽ��ֵ
���������ǰ���8bitλ�����rawͼ��


### step 5
�������������-p���������Ըı�λ����Ϣ
-p [8-32] ָ������λ��
�������´���һ��10bitλ���ͼ����������������
raw_info -f f:\test\1280x1024_10.raw -p 10
�õ�����Ϣ����

```
src file is f:\test\1280x1024_10.raw
pixel_num is 1310720
pixel_min is 78
pixel_max is 418
pixel_aver is 284.21031188964844
```

### step 6
�߼�ѡ��
-d ��ӡ������Ϣ
-a �򿪸߼�����
-t [��ֵ] ָ��������ֵ

�����и�Ϊ��
raw_info -f f:\test\1280x1024.raw -a
���ļ�ͬ��Ŀ¼��������� xxx_info.txt ���ı�����������

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
�����˼�����Ϣ���ֱ���
pixel_max_num��������ص�ĸ���
pixel_min_num����С���ص�ĸ���
pixel_variance��������ֵ����
pixel_std_dev��������ֵ��׼��
pixel_th_above_num������ֵ֮�ϵ����ص�ĸ�������������ֵ�㣬���û��-t����������ֵ��0
