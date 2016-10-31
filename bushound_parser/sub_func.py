#coding=utf-8
##	-------------------------------------------------------------------------------------
##	控制命令 U3VC 的格式是固定的
##	--最开始的4byte是固定的 "55 33 56 43" ，表示 U3VC
##	--接下来的4byte是statue和command
##	--接下来的4byte是length和request_id
##	----如果是读命令，那接下来是8byte寄存器地址和2byte保留字和2byte数据长度
##	----如果是读反馈命令，那接下来是xbyte返回数据
##	----如果是写命令，那接下来是8byte寄存器地址和xbyte数据
##	----如果是写反馈命令，那接下来是2byte保留字和2byte接收的数据长度
##	-------------------------------------------------------------------------------------

def u3vc_proc(*params) :

	##	===============================================================================================
	##	ref ***save parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	传入参数
	##	-------------------------------------------------------------------------------------
	debug	= params[0];
	first_byte_pos	= params[1];
	line_cnt		= params[2];
	file_content	= params[3];

	ret	= [0,"null"];
	if(debug==1):	print("here is u3vc proc");

	##	===============================================================================================
	##	ref ***catch status & command from u3vc***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	bushound log 日志中，每一行只有4组数据，每一组数据宽度是13byte
	##	--13byte中，最后2个byte是空字符
	##	-------------------------------------------------------------------------------------
	line_content	= file_content[line_cnt];
	line_content	= line_content[first_byte_pos:first_byte_pos+13*4];
	if(debug==1):	print("here is u3vc proc,line_content is",line_content);

	##	-------------------------------------------------------------------------------------
	##	提取 status 和 command 信息
	##	-------------------------------------------------------------------------------------
	status	= line_content[13:13+5]
	if(debug==1):	print("here is u3vc proc,status is",status);

	command	= line_content[13+6:13+11]
	if(debug==1):	print("here is u3vc proc,command is",command);

	##	===============================================================================================
	##	ref ***parse command status***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	解析command
	##	-------------------------------------------------------------------------------------
	if(command=="00 08"):
		command_ascii	= "Read";
	elif(command=="01 08"):
		command_ascii	= "ReadAck";
	elif(command=="02 08"):
		command_ascii	= "Write";
	elif(command=="03 08"):
		command_ascii	= "WriteAck";
	elif(command=="05 08"):
		command_ascii	= "PendingAck";
	elif(command=="00 0c"):
		command_ascii	= "Event";
	elif(command=="01 0c"):
		command_ascii	= "EventAck";
	else:
		command_ascii	= "NA";

	##	-------------------------------------------------------------------------------------
	##	解析status
	#	-------------------------------------------------------------------------------------
	if(command=="00 00"):
		status_ascii	= "OK";
	else:
		status_ascii	= "FAIL";

	##	-------------------------------------------------------------------------------------
	##	如果反馈有错误，说明上一条操作失败，立即返回
	#	-------------------------------------------------------------------------------------
	if(command=="ReadAck" or command=="WriteAck"):
		if(status_ascii=="FAIL"):
			ret	= [line_cnt,command+" "+status_ascii];
			return ret;

	##	===============================================================================================
	##	ref ***pick up parameter from each command***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	分别对每个命令，截取不同的信息
	##	-------------------------------------------------------------------------------------
	if(command_ascii=="Read"):
		##	-------------------------------------------------------------------------------------
		##	读地址有8byte，但是我们只读4byte
		##	-------------------------------------------------------------------------------------
		addr	= line_content[48:50]+line_content[45:47]+line_content[42:44]+line_content[39:41];
#		addr	= int(addr);
		if(debug==1):	print("here is u3vc proc,read_addr is",addr);
		##	-------------------------------------------------------------------------------------
		##	如果已经是文件末尾，就不要再读了，直接返回空值
		##	-------------------------------------------------------------------------------------
		if(line_cnt==len(file_content)-1):
			ret	= [line_cnt,"data not enough"];
			return	ret;
		line_content	= file_content[line_cnt+1];
		line_content	= line_content[first_byte_pos:first_byte_pos+13*4];
		read_length		=line_content[22:24]+line_content[19:21];
		if(debug==1):	print("here is u3vc proc,read_length is",read_length);

	elif(command_ascii=="ReadAck"):
		##	-------------------------------------------------------------------------------------
		##	读反馈只读一行数据，因此只会返回4byte寄存器数据
		##	-------------------------------------------------------------------------------------
		read_ack_data	= line_content[48:50]+line_content[45:47]+line_content[42:44]+line_content[39:41];
#		read_ack_data	= int(read_ack_data);
		if(debug==1):	print("here is u3vc proc,read_ack_data is",read_ack_data);

	elif(command_ascii=="Write"):
		##	-------------------------------------------------------------------------------------
		##	写地址有8byte，但是我们只读4byte
		##	--写数据可以有很多，但我们只读4bye
		##	-------------------------------------------------------------------------------------
		addr		= line_content[48:50]+line_content[45:47]+line_content[42:44]+line_content[39:41];
#		addr		= int(addr);
		if(debug==1):	print("here is u3vc proc,write_addr is",addr);
		##	-------------------------------------------------------------------------------------
		##	如果已经是文件末尾，就不要再读了，直接返回空值
		##	-------------------------------------------------------------------------------------
		if(line_cnt==len(file_content)-1):
			ret	= [line_cnt,"data not enough"];
			return	ret;
		line_content	= file_content[line_cnt+1];
		line_content	= line_content[first_byte_pos:first_byte_pos+13*4];
		write_data		= line_content[22:24]+line_content[19:21]+line_content[16:18]+line_content[13:15];
		if(debug==1):	print("here is u3vc proc,write_data is",write_data);

	elif(command_ascii=="WriteAck"):
		##	-------------------------------------------------------------------------------------
		##	读反馈只读一行数据，因此只会返回4byte寄存器数据
		##	-------------------------------------------------------------------------------------
		write_ack_length	= line_content[48:50]+line_content[45:47];
#		write_ack_length	= int(write_ack_length);
		if(debug==1):	print("here is u3vc proc,write_ack_length is",write_ack_length);

	##	===============================================================================================
	##	ref ***search regs corresponding to addr***
	##	===============================================================================================
	if ((command_ascii=="Read") or (command_ascii=="Write")):
		##	-------------------------------------------------------------------------------------
		##	地址列表中都是大写的地址，因此要将add转换为大写
		##	-------------------------------------------------------------------------------------
		addr	= addr.upper();
		if(addr[2:4]=="00"):
			if(addr[4:8]=="0000"):			reg_name	= "GenCP Version"               ;
			elif(addr[4:8]=="0004"):		reg_name	= "Manufacturer Name"           ;
			elif(addr[4:8]=="0044"):		reg_name	= "Model Name"                  ;
			elif(addr[4:8]=="0084"):		reg_name	= "Family Name"                 ;
			elif(addr[4:8]=="00C4"):		reg_name	= "Device Version"              ;
			elif(addr[4:8]=="0104"):		reg_name	= "Manufacturer Info"           ;
			elif(addr[4:8]=="0144"):		reg_name	= "Serial Number"               ;
			elif(addr[4:8]=="0184"):		reg_name	= "User Defined Name"           ;
			elif(addr[4:8]=="01C4"):		reg_name	= "Device Capability"           ;
			elif(addr[4:8]=="01CC"):		reg_name	= "Maximum Device Response Time";
			elif(addr[4:8]=="01D0"):		reg_name	= "Manifest Table Address"      ;
			elif(addr[4:8]=="01D8"):		reg_name	= "SBRM Address"                ;
			elif(addr[4:8]=="01E0"):		reg_name	= "Device Configuration"        ;
			elif(addr[4:8]=="01E8"):		reg_name	= "Heartbeat Timeout"           ;
			elif(addr[4:8]=="01EC"):		reg_name	= "Message Channel ID"          ;
			elif(addr[4:8]=="01F0"):		reg_name	= "Timestamp"                   ;
			elif(addr[4:8]=="01F8"):		reg_name	= "Timestamp Latch"             ;
			elif(addr[4:8]=="01FC"):		reg_name	= "Timestamp Increment"         ;
			elif(addr[4:8]=="0204"):		reg_name	= "Access Privilege"            ;
			elif(addr[4:8]=="0208"):		reg_name	= "Protocol Endianess"          ;
			elif(addr[4:8]=="020C"):		reg_name	= "Implementation Endianess"    ;
			elif(addr[4:8]=="0210"):		reg_name	= "Reserved Register Space"     ;
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="02"):
			if(addr[4:8]=="0000"):			reg_name	= "SI Info"                        ;
			elif(addr[4:8]=="0004"):		reg_name	= "SI Control"                     ;
			elif(addr[4:8]=="0008"):		reg_name	= "SI Required Payload Size"       ;
			elif(addr[4:8]=="0010"):		reg_name	= "SI Required Leader Size"        ;
			elif(addr[4:8]=="0014"):		reg_name	= "SI Required Trailer Size"       ;
			elif(addr[4:8]=="0018"):		reg_name	= "SI Maximum Leader Size"         ;
			elif(addr[4:8]=="001C"):		reg_name	= "SI Payload Transfer Size"       ;
			elif(addr[4:8]=="0020"):		reg_name	= "SI Payload Transfer Count"      ;
			elif(addr[4:8]=="0024"):		reg_name	= "SI Payload Final Transfer1 Size";
			elif(addr[4:8]=="0028"):		reg_name	= "SI Payload Final Transfer2 Size";
			elif(addr[4:8]=="002C"):		reg_name	= "SI Maximum Trailer Size"        ;
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="30"):
			if(addr[4:8]=="0000"):			reg_name	= "DeviceFirmwareVersion";
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="40"):
			if(addr[4:8]=="0000"):			reg_name	= "SensorWidthImplemented"                        ;
			elif(addr[4:8]=="0004"):		reg_name	= "SensorHeightImplemented"                       ;
			elif(addr[4:8]=="0008"):		reg_name	= "WidthMaxImplemented"                           ;
			elif(addr[4:8]=="000C"):		reg_name	= "HeightMaxImplemented"                          ;
			elif(addr[4:8]=="0010"):		reg_name	= "RegionSelectorImplemented"                     ;
			elif(addr[4:8]=="0014"):		reg_name	= "WidthImplemented_Region0"                      ;
			elif(addr[4:8]=="0018"):		reg_name	= "HeightImplemented_Region0"                     ;
			elif(addr[4:8]=="001C"):		reg_name	= "OffsetXImplemented_Region0"                    ;
			elif(addr[4:8]=="0020"):		reg_name	= "OffsetYImplemented_Region0"                    ;
			elif(addr[4:8]=="0024"):		reg_name	= "PixelFormatImplemented"                        ;
			elif(addr[4:8]=="0028"):		reg_name	= "TestPatternGeneratorSelectorImplemented"       ;
			elif(addr[4:8]=="002C"):		reg_name	= "TestPatternImplemented_Region0"                ;
			elif(addr[4:8]=="0030"):		reg_name	= "AcquisitionModeImplemented"                    ;
			elif(addr[4:8]=="0034"):		reg_name	= "AcquisitionStartImplemented"                   ;
			elif(addr[4:8]=="0038"):		reg_name	= "AcquisitionStopImplemented"                    ;
			elif(addr[4:8]=="003C"):		reg_name	= "TriggerSelectorImplemented"                    ;
			elif(addr[4:8]=="0040"):		reg_name	= "TriggerModeImplemented_FrameStart"             ;
			elif(addr[4:8]=="0044"):		reg_name	= "TriggerSoftwareImplemented_FrameStart"         ;
			elif(addr[4:8]=="0048"):		reg_name	= "TriggerSourceImplemented_FrameStart"           ;
			elif(addr[4:8]=="004C"):		reg_name	= "TriggerActivationImplemented_FrameStart"       ;
			elif(addr[4:8]=="0050"):		reg_name	= "TriggerDelayImplemented_FrameStart"            ;
			elif(addr[4:8]=="0054"):		reg_name	= "TriggerFilterRisingEdgeImplemented_FrameStart" ;
			elif(addr[4:8]=="0058"):		reg_name	= "TriggerFilterFallingEdgeImplemented_FrameStart";
			elif(addr[4:8]=="005C"):		reg_name	= "ExposureModeImplemented"                       ;
			elif(addr[4:8]=="0060"):		reg_name	= "ExposureTimeImplemented"                       ;
			elif(addr[4:8]=="0064"):		reg_name	= "ExposureAutoImplemented"                       ;
			elif(addr[4:8]=="0068"):		reg_name	= "AutoExposureTimeMinImplemented"                ;
			elif(addr[4:8]=="006C"):		reg_name	= "AutoExposureTimeMaxImplemented"                ;
			elif(addr[4:8]=="0070"):		reg_name	= "AAROIWidthImplemented"                         ;
			elif(addr[4:8]=="0074"):		reg_name	= "AAROIHeightImplemented"                        ;
			elif(addr[4:8]=="0078"):		reg_name	= "AAROIOffsetXImplemented"                       ;
			elif(addr[4:8]=="007C"):		reg_name	= "AAROIOffsetYImplemented"                       ;
			elif(addr[4:8]=="0080"):		reg_name	= "ExpectedGrayValueImplemented"                  ;
			elif(addr[4:8]=="0084"):		reg_name	= "LineSelectorImplemented"                       ;
			elif(addr[4:8]=="0088"):		reg_name	= "LineModeImplemented_Line0"                     ;
			elif(addr[4:8]=="008C"):		reg_name	= "LineModeImplemented_Line1"                     ;
			elif(addr[4:8]=="0090"):		reg_name	= "LineModeImplemented_Line2"                     ;
			elif(addr[4:8]=="0094"):		reg_name	= "LineModeImplemented_Line3"                     ;
			elif(addr[4:8]=="0098"):		reg_name	= "LineInverterImplemented_Line0"                 ;
			elif(addr[4:8]=="009C"):		reg_name	= "LineInverterImplemented_Line1"                 ;
			elif(addr[4:8]=="00A0"):		reg_name	= "LineInverterImplemented_Line2"                 ;
			elif(addr[4:8]=="00A4"):		reg_name	= "LineInverterImplemented_Line3"                 ;
			elif(addr[4:8]=="00A8"):		reg_name	= "LineSourceImplemented_Line0"                   ;
			elif(addr[4:8]=="00AC"):		reg_name	= "LineSourceImplemented_Line1"                   ;
			elif(addr[4:8]=="00B0"):		reg_name	= "LineSourceImplemented_Line2"                   ;
			elif(addr[4:8]=="00B4"):		reg_name	= "LineSourceImplemented_Line3"                   ;
			elif(addr[4:8]=="00B8"):		reg_name	= "LineStatusImplemented_Line0"                   ;
			elif(addr[4:8]=="00BC"):		reg_name	= "LineStatusImplemented_Line1"                   ;
			elif(addr[4:8]=="00C0"):		reg_name	= "LineStatusImplemented_Line2"                   ;
			elif(addr[4:8]=="00C4"):		reg_name	= "LineStatusImplemented_Line3"                   ;
			elif(addr[4:8]=="00C8"):		reg_name	= "LineStatusAllImplemented"                      ;
			elif(addr[4:8]=="00CC"):		reg_name	= "UserOutputSelectorImplemented"                 ;
			elif(addr[4:8]=="00D0"):		reg_name	= "UserOutputValueImplemented_Output0"            ;
			elif(addr[4:8]=="00D4"):		reg_name	= "UserOutputValueImplemented_Output1"            ;
			elif(addr[4:8]=="00D8"):		reg_name	= "UserOutputValueImplemented_Output2"            ;
			elif(addr[4:8]=="00DC"):		reg_name	= "EventSelectorImplemented"                      ;
			elif(addr[4:8]=="00E0"):		reg_name	= "Reserved"                                      ;
			elif(addr[4:8]=="00E4"):		reg_name	= "Reserved"                                      ;
			elif(addr[4:8]=="00E8"):		reg_name	= "EventNotificationImplemented_ExposureEnd"      ;
			elif(addr[4:8]=="00EC"):		reg_name	= "Reserved"                                      ;
			elif(addr[4:8]=="00F0"):		reg_name	= "EventFrameIDImplemented_ExposureEnd"           ;
			elif(addr[4:8]=="00F4"):		reg_name	= "GainSelectorImplemented"                       ;
			elif(addr[4:8]=="00F8"):		reg_name	= "GainImplemented_All"                           ;
			elif(addr[4:8]=="00FC"):		reg_name	= "GainAutoImplemented_All"                       ;
			elif(addr[4:8]=="0100"):		reg_name	= "AutoGainMinImplemented_All"                    ;
			elif(addr[4:8]=="0104"):		reg_name	= "AutoGainMaxImplemented_All"                    ;
			elif(addr[4:8]=="0108"):		reg_name	= "BalanceRatioSelectorImplemented"               ;
			elif(addr[4:8]=="010C"):		reg_name	= "BalanceRatioImplemented_Red"                   ;
			elif(addr[4:8]=="0110"):		reg_name	= "BalanceRatioImplemented_Green"                 ;
			elif(addr[4:8]=="0114"):		reg_name	= "BalanceRatioImplemented_Blue"                  ;
			elif(addr[4:8]=="0118"):		reg_name	= "BalanceWhiteAutoImplemented"                   ;
			elif(addr[4:8]=="011C"):		reg_name	= "AWBLampHouseImplemented"                       ;
			elif(addr[4:8]=="0120"):		reg_name	= "AWBROIWidthImplemented"                        ;
			elif(addr[4:8]=="0124"):		reg_name	= "AWBROIHeightImplemented"                       ;
			elif(addr[4:8]=="0128"):		reg_name	= "AWBROIOffsetXImplemented"                      ;
			elif(addr[4:8]=="012C"):		reg_name	= "AWBROIOffsetYImplemented"                      ;
			elif(addr[4:8]=="0130"):		reg_name	= "DeadPixelCorrectImplemented"                   ;
			elif(addr[4:8]=="0134"):		reg_name	= "LUTSelectorImplemented"                        ;
			elif(addr[4:8]=="0138"):		reg_name	= "LUTValueAllImplemented_Luminance"             ;
			elif(addr[4:8]=="013C"):		reg_name	= "DeviceLinkSelectorImplemented"                 ;
			elif(addr[4:8]=="0140"):		reg_name	= "DeviceLinkThroughputLimitModeImplemented_Link0";
			elif(addr[4:8]=="0144"):		reg_name	= "DeviceLinkThroughputLimitImplemented_Link0"    ;
			elif(addr[4:8]=="0148"):		reg_name	= "DeviceLinkCurrentThroughputImplemented_Link0"  ;
			elif(addr[4:8]=="014C"):		reg_name	= "UserSetSelectorImplemented"                    ;
			elif(addr[4:8]=="0150"):		reg_name	= "UserSetLoadImplemented_Default"                ;
			elif(addr[4:8]=="0154"):		reg_name	= "UserSetLoadImplemented_UserSet0"               ;
			elif(addr[4:8]=="0158"):		reg_name	= "UserSetLoadImplemented_UserSet1"              ;
			elif(addr[4:8]=="015C"):		reg_name	= "UserSetSaveImplemented_UserSet0"               ;
			elif(addr[4:8]=="0160"):		reg_name	= "UserSetSaveImplemented_UserSet1"               ;
			elif(addr[4:8]=="0164"):		reg_name	= "UserSetDefaultImplemented"                     ;
			elif(addr[4:8]=="0168"):		reg_name	= "ChunkModeActiveImplemented"                    ;
			elif(addr[4:8]=="016C"):		reg_name	= "ChunkSelectorImplemented"                      ;
			elif(addr[4:8]=="0170"):		reg_name	= "ChunkEnableImplemented_FrameID"                ;
			elif(addr[4:8]=="0174"):		reg_name	= "ChunkEnableImplemented_Timestamp"              ;
			elif(addr[4:8]=="0178"):		reg_name	= "ColorCorrectionParamImplemented"               ;
			elif(addr[4:8]=="017C"):		reg_name	= "DeviceResetImplemented"                        ;
			elif(addr[4:8]=="0180"):		reg_name	= "TestPendingAckImplemented"                     ;
			elif(addr[4:8]=="0184"):		reg_name	= "GammaParamImplemented"                         ;
			elif(addr[4:8]=="0188"):		reg_name	= "ContrastParamImplemented"                      ;
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="50"):
			if(addr[4:8]=="0000"):			reg_name	= "RegionSelectorInfo"                     ;
			elif(addr[4:8]=="0004"):		reg_name	= "PixelFormatInfo_High"                   ;
			elif(addr[4:8]=="0008"):		reg_name	= "PixelFormatInfo_Low"                    ;
			elif(addr[4:8]=="000C"):		reg_name	= "TestPatternGeneratorSelectorInfo"       ;
			elif(addr[4:8]=="0010"):		reg_name	= "TestPatternInfo_Region0"                ;
			elif(addr[4:8]=="0014"):		reg_name	= "AcquisitionModeInfo"                    ;
			elif(addr[4:8]=="0018"):		reg_name	= "TriggerSelectorInfo"                    ;
			elif(addr[4:8]=="001C"):		reg_name	= "TriggerModeInfo_FrameStart"             ;
			elif(addr[4:8]=="0020"):		reg_name	= "TriggerSourceInfo_FrameStart"           ;
			elif(addr[4:8]=="0024"):		reg_name	= "TriggerActivationInfo_FrameStart"       ;
			elif(addr[4:8]=="0028"):		reg_name	= "ExposureModeInfo"                       ;
			elif(addr[4:8]=="002C"):		reg_name	= "ExposureAutoInfo"                       ;
			elif(addr[4:8]=="0030"):		reg_name	= "LineSelectorInfo"                       ;
			elif(addr[4:8]=="0034"):		reg_name	= "LineModeInfo_Line0"                     ;
			elif(addr[4:8]=="0038"):		reg_name	= "LineModeInfo_Line1"                     ;
			elif(addr[4:8]=="003C"):		reg_name	= "LineModeInfo_Line2"                     ;
			elif(addr[4:8]=="0040"):		reg_name	= "LineModeInfo_Line3"                     ;
			elif(addr[4:8]=="0044"):		reg_name	= "LineSourceinfo_Line0"                   ;
			elif(addr[4:8]=="0048"):		reg_name	= "LineSourceinfo_Line1"                   ;
			elif(addr[4:8]=="004C"):		reg_name	= "LineSourceinfo_Line2"                   ;
			elif(addr[4:8]=="0050"):		reg_name	= "LineSourceinfo_Line3"                   ;
			elif(addr[4:8]=="0054"):		reg_name	= "UserOutputSelectorInfo"                 ;
			elif(addr[4:8]=="0058"):		reg_name	= "EventSelectorInfo"                      ;
			elif(addr[4:8]=="005C"):		reg_name	= "GainSelectorInfo"                       ;
			elif(addr[4:8]=="0060"):		reg_name	= "GainAutoInfo_All"                       ;
			elif(addr[4:8]=="0064"):		reg_name	= "BalanceRatioSelectorInfo"               ;
			elif(addr[4:8]=="0068"):		reg_name	= "BalanceWhiteAutoInfo"                   ;
			elif(addr[4:8]=="006C"):		reg_name	= "AWBLampHouseInfo"                       ;
			elif(addr[4:8]=="0070"):		reg_name	= "DeadPixelCorrectInfo"                   ;
			elif(addr[4:8]=="0074"):		reg_name	= "LUTSelectorInfo"                        ;
			elif(addr[4:8]=="0078"):		reg_name	= "DeviceLinkThroughputLimitModeInfo_Link0";
			elif(addr[4:8]=="007C"):		reg_name	= "UserSetSelectorInfo"                    ;
			elif(addr[4:8]=="0080"):		reg_name	= "UserSetDefaultInfo"                     ;
			elif(addr[4:8]=="0084"):		reg_name	= "ChunkSelectorInfo"                      ;
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="60"):
			if(addr[4:8]=="0000"):			reg_name	= "WidthMax"                              ;
			elif(addr[4:8]=="0004"):		reg_name	= "HeightMax"                             ;
			elif(addr[4:8]=="0008"):		reg_name	= "WidthMax_Region0"                      ;
			elif(addr[4:8]=="000C"):		reg_name	= "WidthMin_Region0"                      ;
			elif(addr[4:8]=="0010"):		reg_name	= "HeightMax_Region0"                     ;
			elif(addr[4:8]=="0014"):		reg_name	= "HeightMin_Region0"                     ;
			elif(addr[4:8]=="0018"):		reg_name	= "OffsetXMin_Region0"                    ;
			elif(addr[4:8]=="001C"):		reg_name	= "OffsetYMin_Region0"                    ;
			elif(addr[4:8]=="0020"):		reg_name	= "TriggerDelayMax_FrameStart"            ;
			elif(addr[4:8]=="0024"):		reg_name	= "TriggerDelayMin_FrameStart"            ;
			elif(addr[4:8]=="0028"):		reg_name	= "TriggerFilterRisingEdgeMax_FrameStart" ;
			elif(addr[4:8]=="002C"):		reg_name	= "TriggerFilterRisingEdgeMin_FrameStart" ;
			elif(addr[4:8]=="0030"):		reg_name	= "TriggerFilterFallingEdgeMax_FrameStart";
			elif(addr[4:8]=="0034"):		reg_name	= "TriggerFilterFallingEdgeMin_FrameStart";
			elif(addr[4:8]=="0038"):		reg_name	= "ExposureTimeMax"                       ;
			elif(addr[4:8]=="003C"):		reg_name	= "ExposureTimeMin"                       ;
			elif(addr[4:8]=="0040"):		reg_name	= "AutoExposureTimeMinMax"                ;
			elif(addr[4:8]=="0044"):		reg_name	= "AutoExposureTimeMinMin"                ;
			elif(addr[4:8]=="0048"):		reg_name	= "AutoExposureTimeMaxMax"                ;
			elif(addr[4:8]=="004C"):		reg_name	= "AutoExposureTimeMaxMin"                ;
			elif(addr[4:8]=="0050"):		reg_name	= "AAROIWidthMin"                         ;
			elif(addr[4:8]=="0054"):		reg_name	= "AAROIHeightMin"                        ;
			elif(addr[4:8]=="0058"):		reg_name	= "AAROIOffsetXMin"                       ;
			elif(addr[4:8]=="005C"):		reg_name	= "AAROIOffsetYMin"                       ;
			elif(addr[4:8]=="0060"):		reg_name	= "Reserved"                              ;
			elif(addr[4:8]=="0064"):		reg_name	= "Reserved"                              ;
			elif(addr[4:8]=="0068"):		reg_name	= "GainMax_All"                           ;
			elif(addr[4:8]=="006C"):		reg_name	= "GainMin_All"                           ;
			elif(addr[4:8]=="0070"):		reg_name	= "AutoGainMinMax_All"                    ;
			elif(addr[4:8]=="0074"):		reg_name	= "AutoGainMinMin_All"                    ;
			elif(addr[4:8]=="0078"):		reg_name	= "AutoGainMaxMax_All"                    ;
			elif(addr[4:8]=="007C"):		reg_name	= "AutoGainMaxMin_All"                    ;
			elif(addr[4:8]=="0080"):		reg_name	= "BalanceRatioMax_Red"                   ;
			elif(addr[4:8]=="0084"):		reg_name	= "BalanceRatioMin_Red"                   ;
			elif(addr[4:8]=="0088"):		reg_name	= "BalanceRatioMax_Green"                 ;
			elif(addr[4:8]=="008C"):		reg_name	= "BalanceRatioMin_Green"                 ;
			elif(addr[4:8]=="0090"):		reg_name	= "BalanceRatioMax_Blue"                  ;
			elif(addr[4:8]=="0094"):		reg_name	= "BalanceRatioMin_Blue"                  ;
			elif(addr[4:8]=="0098"):		reg_name	= "AWBROIWidth_Min"                       ;
			elif(addr[4:8]=="009C"):		reg_name	= "AWBROIHeight_Min"                      ;
			elif(addr[4:8]=="00A0"):		reg_name	= "AWBROIOffsetX_Min"                     ;
			elif(addr[4:8]=="00A4"):		reg_name	= "AWBROIOffsetY_Min"                     ;
			elif(addr[4:8]=="00A8"):		reg_name	= "DeviceLinkSelector_Max"                ;
			elif(addr[4:8]=="00AC"):		reg_name	= "DeviceLinkSelector_Min"                ;
			elif(addr[4:8]=="00B0"):		reg_name	= "DeviceLinkThroughputLimitMax_Link0"    ;
			elif(addr[4:8]=="00B4"):		reg_name	= "DeviceLinkThroughputLimitMin_Link0"    ;
			elif(addr[4:8]=="00B8"):		reg_name	= "TestPendingAck_Max"                    ;
			elif(addr[4:8]=="00BC"):		reg_name	= "TestPendingAck_Min"                    ;
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="70"):
			if(addr[4:8]=="0000"):			reg_name	= "WidthStep_Region0"                           ;
			elif(addr[4:8]=="0004"):		reg_name	= "HeightStep_Region0"                          ;
			elif(addr[4:8]=="0008"):		reg_name	= "OffsetXStep_Region0"                         ;
			elif(addr[4:8]=="000C"):		reg_name	= "OffsetYStep_Region0"                         ;
			elif(addr[4:8]=="0010"):		reg_name	= "TriggerDelayPrecision_FrameStart"            ;
			elif(addr[4:8]=="0014"):		reg_name	= "TriggerFilterRisingEdgePrecision_FrameStart" ;
			elif(addr[4:8]=="0018"):		reg_name	= "TriggerFilterFallingEdgePrecision_FrameStart";
			elif(addr[4:8]=="001C"):		reg_name	= "ExposureTimePrecision"                       ;
			elif(addr[4:8]=="0020"):		reg_name	= "AAROIWidthStep"                              ;
			elif(addr[4:8]=="0024"):		reg_name	= "AAROIHeightStep"                             ;
			elif(addr[4:8]=="0028"):		reg_name	= "AAROIOffsetXStep"                            ;
			elif(addr[4:8]=="002C"):		reg_name	= "AAROIOffsetYStep"                            ;
			elif(addr[4:8]=="0030"):		reg_name	= "ExpectedGrayValueStep"                       ;
			elif(addr[4:8]=="0034"):		reg_name	= "GainPrecision_All"                           ;
			elif(addr[4:8]=="0038"):		reg_name	= "AutoGainMinPrecision_All"                    ;
			elif(addr[4:8]=="003C"):		reg_name	= "AutoGainMaxPrecision_All"                    ;
			elif(addr[4:8]=="0040"):		reg_name	= "BalanceRatioPrecision_Red"                   ;
			elif(addr[4:8]=="0044"):		reg_name	= "BalanceRatioPrecision_Green"                 ;
			elif(addr[4:8]=="0048"):		reg_name	= "BalanceRatioPrecision_Blue"                  ;
			elif(addr[4:8]=="004C"):		reg_name	= "AWBROIWidth_Step"                            ;
			elif(addr[4:8]=="0050"):		reg_name	= "AWBROIHeight_Step"                           ;
			elif(addr[4:8]=="0054"):		reg_name	= "AWBROIOffsetX_Step"                          ;
			elif(addr[4:8]=="0058"):		reg_name	= "AWBROIOffsetY_Step"                          ;
			elif(addr[4:8]=="005C"):		reg_name	= "LUTValueAll_Length"                          ;
			elif(addr[4:8]=="0060"):		reg_name	= "DeviceLinkSelector_Step"                     ;
			elif(addr[4:8]=="0064"):		reg_name	= "DeviceLinkThroughputLimitStep_Link0"         ;
			elif(addr[4:8]=="0068"):		reg_name	= "TestPendingAck_Step"                         ;
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="80"):
			if(addr[4:8]=="0000"):			reg_name	= "AcquisitionMode"                  ;
			elif(addr[4:8]=="0004"):		reg_name	= "AcquisitionStart"                 ;
			elif(addr[4:8]=="0008"):		reg_name	= "TriggerSoftware_FrameStart"       ;
			elif(addr[4:8]=="000C"):		reg_name	= "ExposureMode"                     ;
			elif(addr[4:8]=="0010"):		reg_name	= "LineStatus_Line0"                 ;
			elif(addr[4:8]=="0014"):		reg_name	= "LineStatus_Line1"                 ;
			elif(addr[4:8]=="0018"):		reg_name	= "LineStatus_Line2"                 ;
			elif(addr[4:8]=="001C"):		reg_name	= "LineStatus_Line3"                 ;
			elif(addr[4:8]=="0020"):		reg_name	= "LineStatusAll"                    ;
			elif(addr[4:8]=="0024"):		reg_name	= "Reserved"                         ;
			elif(addr[4:8]=="0028"):		reg_name	= "EventNotification_ExposureEnd"    ;
			elif(addr[4:8]=="002C"):		reg_name	= "DeviceLinkCurrentThroughput_Link0";
			elif(addr[4:8]=="0030"):		reg_name	= "UserSetLoad_Default"              ;
			elif(addr[4:8]=="0034"):		reg_name	= "UserSetLoad_UserSet0"             ;
			elif(addr[4:8]=="0038"):		reg_name	= "UserSetLoad_UserSet1"             ;
			elif(addr[4:8]=="003C"):		reg_name	= "UserSetSave_UserSet0"             ;
			elif(addr[4:8]=="0040"):		reg_name	= "UserSetSave_UserSet1"             ;
			elif(addr[4:8]=="0044"):		reg_name	= "UserSetDefault"                   ;
			elif(addr[4:8]=="0048"):		reg_name	= "DeviceReset"                      ;
			elif(addr[4:8]=="004C"):		reg_name	= "TestPendingAck"                   ;
			elif(addr[4:8]=="0050"):		reg_name	= "SensorWidth"                      ;
			elif(addr[4:8]=="0054"):		reg_name	= "SensorHeight"                     ;
			elif(addr[4:8]=="0058"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="005C"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="0060"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="0064"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="0068"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="006C"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="0070"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="0074"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="0078"):		reg_name	= "ColorCorrectionParam";
			elif(addr[4:8]=="007C"):		reg_name	= "FactorySettingVersion"         ;
			elif(addr[4:8]=="00BC"):		reg_name	= "SensorFlag"                    ;
			elif(addr[4:8]=="00C0"):		reg_name	= "GammaParam"                    ;
			elif(addr[4:8]=="00C4"):		reg_name	= "ContrastParam"                 ;
			elif(addr[4:8]=="00C8"):		reg_name	= "RedAdjustMaxValueD75"          ;
			elif(addr[4:8]=="00CC"):		reg_name	= "BlueAdjustMinValueD75"         ;
			elif(addr[4:8]=="00D0"):		reg_name	= "RedAdjustMaxValueD65"          ;
			elif(addr[4:8]=="00D4"):		reg_name	= "BlueAdjustMinValueD65"         ;
			elif(addr[4:8]=="00D8"):		reg_name	= "RedAdjustMaxValueD50"          ;
			elif(addr[4:8]=="00DC"):		reg_name	= "BlueAdjustMinValueD50"         ;
			elif(addr[4:8]=="00E0"):		reg_name	= "RedAdjustMaxValueFlu"          ;
			elif(addr[4:8]=="00E4"):		reg_name	= "BlueAdjustMinValueFlu"         ;
			elif(addr[4:8]=="00E8"):		reg_name	= "RedAdjustMaxValueU30"          ;
			elif(addr[4:8]=="00EC"):		reg_name	= "BlueAdjustMinValueU30"         ;
			elif(addr[4:8]=="00F0"):		reg_name	= "RedAdjustMaxValueIncandescent" ;
			elif(addr[4:8]=="00F4"):		reg_name	= "BlueAdjustMinValueIncandescent";
			else: 							reg_name	= "UnKnown RegAddr"	;

		elif(addr[2:4]=="90"):
			if(addr[4:8]=="0000"):			reg_name	= "Reserved1"                          ;
			elif(addr[4:8]=="0004"):		reg_name	= "Reserved2"                          ;
			elif(addr[4:8]=="0008"):		reg_name	= "Width_Region0"                      ;
			elif(addr[4:8]=="000C"):		reg_name	= "Height_Region0"                     ;
			elif(addr[4:8]=="0010"):		reg_name	= "OffsetX_Region0"                    ;
			elif(addr[4:8]=="0014"):		reg_name	= "OffsetY_Region0"                    ;
			elif(addr[4:8]=="0018"):		reg_name	= "PixelFormat"                        ;
			elif(addr[4:8]=="001C"):		reg_name	= "TestPattern_Region0"                ;
			elif(addr[4:8]=="0020"):		reg_name	= "TriggerMode_FrameStart"             ;
			elif(addr[4:8]=="0024"):		reg_name	= "TriggerSource_FrameStart"           ;
			elif(addr[4:8]=="0028"):		reg_name	= "TriggerActivation_FrameStart"       ;
			elif(addr[4:8]=="002C"):		reg_name	= "TriggerDelay_FrameStart"            ;
			elif(addr[4:8]=="0030"):		reg_name	= "TriggerFilterRisingEdge_FrameStart" ;
			elif(addr[4:8]=="0034"):		reg_name	= "TriggerFilterFallingEdge_FrameStart";
			elif(addr[4:8]=="0038"):		reg_name	= "ExposureTime"                       ;
			elif(addr[4:8]=="003C"):		reg_name	= "ExposureAuto"                       ;
			elif(addr[4:8]=="0040"):		reg_name	= "AutoExposureTimeMin"                ;
			elif(addr[4:8]=="0044"):		reg_name	= "AutoExposureTimeMax"                ;
			elif(addr[4:8]=="0048"):		reg_name	= "AAROIWidth"                         ;
			elif(addr[4:8]=="004C"):		reg_name	= "AAROIHeight"                        ;
			elif(addr[4:8]=="0050"):		reg_name	= "AAROIOffsetX"                       ;
			elif(addr[4:8]=="0054"):		reg_name	= "AAROIOffsetY"                       ;
			elif(addr[4:8]=="0058"):		reg_name	= "ExpectedGrayValue"                  ;
			elif(addr[4:8]=="005C"):		reg_name	= "LineMode_Line0"                     ;
			elif(addr[4:8]=="0060"):		reg_name	= "LineMode_Line1"                     ;
			elif(addr[4:8]=="0064"):		reg_name	= "LineMode_Line2"                     ;
			elif(addr[4:8]=="0068"):		reg_name	= "LineMode_Line3"                     ;
			elif(addr[4:8]=="006C"):		reg_name	= "LineInverter_Line0"                 ;
			elif(addr[4:8]=="0070"):		reg_name	= "LineInverter_Line1"                 ;
			elif(addr[4:8]=="0074"):		reg_name	= "LineInverter_Line2"                 ;
			elif(addr[4:8]=="0078"):		reg_name	= "LineInverter_Line3"                 ;
			elif(addr[4:8]=="007C"):		reg_name	= "LineSource_Line0"                   ;
			elif(addr[4:8]=="0080"):		reg_name	= "LineSource_Line1"                   ;
			elif(addr[4:8]=="0084"):		reg_name	= "LineSource_Line2"                   ;
			elif(addr[4:8]=="0088"):		reg_name	= "LineSource_Line3"                   ;
			elif(addr[4:8]=="008C"):		reg_name	= "UserOutputValue_Output0"            ;
			elif(addr[4:8]=="0090"):		reg_name	= "UserOutputValue_Output1"            ;
			elif(addr[4:8]=="0094"):		reg_name	= "UserOutputValue_Output2"            ;
			elif(addr[4:8]=="0098"):		reg_name	= "Gain_All"                           ;
			elif(addr[4:8]=="009C"):		reg_name	= "GainAuto_All"                       ;
			elif(addr[4:8]=="00A0"):		reg_name	= "AutoGainMin_All"                    ;
			elif(addr[4:8]=="00A4"):		reg_name	= "AutoGainMax_All"                    ;
			elif(addr[4:8]=="00A8"):		reg_name	= "BalanceRatio_Red"                   ;
			elif(addr[4:8]=="00AC"):		reg_name	= "BalanceRatio_Green"                 ;
			elif(addr[4:8]=="00B0"):		reg_name	= "BalanceRatio_Blue"                  ;
			elif(addr[4:8]=="00B4"):		reg_name	= "BalanceWhiteAuto"                   ;
			elif(addr[4:8]=="00B8"):		reg_name	= "AWBLampHouse"                       ;
			elif(addr[4:8]=="00BC"):		reg_name	= "AWBROIWidth"                        ;
			elif(addr[4:8]=="00C0"):		reg_name	= "AWBROIHeight"                       ;
			elif(addr[4:8]=="00C4"):		reg_name	= "AWBROIOffsetX"                      ;
			elif(addr[4:8]=="00C8"):		reg_name	= "AWBROIOffsetY"                      ;
			elif(addr[4:8]=="00CC"):		reg_name	= "DeadPixelCorrect"                   ;
			elif(addr[4:8]=="00D0"):		reg_name	= "DeviceLinkThroughputLimitMode_Link0";
			elif(addr[4:8]=="00D4"):		reg_name	= "DeviceLinkThroughputLimit_Link0"    ;
			elif(addr[4:8]=="00D8"):		reg_name	= "ChunkModeActive"                    ;
			elif(addr[4:8]=="00DC"):		reg_name	= "ChunkEnable_FrameID"                ;
			elif(addr[4:8]=="00E0"):		reg_name	= "ChunkEnable_Timestamp"              ;
			else: 							reg_name	= "UnKnown RegAddr"	;

		else:
			reg_name	= "UnKnown RegAddr"	;

	##	===============================================================================================
	##	ref ***return result***
	##	===============================================================================================
	if(command_ascii=="Read"):
		ret	= [line_cnt,command_ascii+" "+reg_name+" 0x"+read_length+"Byte"];
		if(debug==1):	print("here is u3vc proc,ret is",ret[1]);
	elif(command_ascii=="ReadAck"):
		ret	= [line_cnt,command_ascii+" 0x"+read_ack_data];
		if(debug==1):	print("here is u3vc proc,ret is",ret[1]);
	elif(command_ascii=="Write"):
		ret	= [line_cnt,command_ascii+" "+reg_name+" 0x"+write_data];
		if(debug==1):	print("here is u3vc proc,ret is",ret[1]);
	elif(command_ascii=="WriteAck"):
		ret	= [line_cnt,command_ascii+" 0x"+write_ack_length+"Byte"];
		if(debug==1):	print("here is u3vc proc,ret is",ret[1]);

	return	ret;



##	-------------------------------------------------------------------------------------
##  Table 7 – Status Codes
##
##  Status Code
##  (Hex)  Name                        Description
##  0x0000 GENCP_SUCCESS               Success
##  0x8001 GENCP_NOT_IMPLEMENTED       Command not implemented in the device.
##  0x8002 GENCP_INVALID_PARAMETER     At least one command parameter of CCD or SCD is invalid or out of range.
##  0x8003 GENCP_INVALID_ADDRESS       Attempt to access a not existing register address.
##  0x8004 GENCP_WRITE_PROTECT         Attempt to write to a read only register.
##  0x8005 GENCP_BAD_ALIGNMENT         Attempt to access registers with an address which is not aligned according to the underlying technology.
##  0x8006 GENCP_ACCESS_DENIED         Attempt to read a non-readable or write a non-writable register address.
##  0x8007 GENCP_BUSY                  The command receiver is currently busy.
##  0x800B GENCP_MSG_TIMEOUT           Timeout waiting for an acknowledge.
##  0x800E GENCP_INVALID_HEADER        The header of the received command is invalid. This includes CCD and SCD fields but not the command payload.
##  0x800F GENCP_WRONG_CONFIG          The current receiver configuration does not allow the execution of the sent command.
##	-------------------------------------------------------------------------------------
##	-------------------------------------------------------------------------------------
##  Table 8 – Command Identifier
##
##  Command Name   command_id
##  READMEM_CMD    0x0800
##  READMEM_ACK    0x0801
##  WRITEMEM_CMD   0x0802
##  WRITEMEM_ACK   0x0803
##  PENDING_ACK    0x0805
##  EVENT_CMD      0x0C00
##  EVENT_ACK      0x0C01
##	-------------------------------------------------------------------------------------
##	-------------------------------------------------------------------------------------
##  Table 9 - ReadMem SCD-Fields
##
##  Width    Offset    Description
##  (Bytes)  (Bytes)
##  ***Prefix***
##  ***CCD (command_id = READMEM_CMD)***
##  8        0         register address 64 bit register address.
##  2        8         Reserved, set to 0
##  2        10        read length Number of bytes to read.
##  ***Postfix***
##	-------------------------------------------------------------------------------------
##	-------------------------------------------------------------------------------------
##  Table 10 - ReadMem Ack SCD-Fields
##
##  Width    Offset    Description
##  (Bytes)  (Bytes)
##  ***Prefix***
##  ***CCD-ACK (command_id = READMEM_ACK)***
##  x        0         Data read from the remote device’s register map. If the number of bytes
##                     read is different than the specified in the relating READMEM_CMD the
##                     status of the READMEM_ACK must indicate the reason.
##  ***Postfix***
##	-------------------------------------------------------------------------------------
##	-------------------------------------------------------------------------------------
##  Table 11 - WriteMem Command SCD-Fields
##
##  Width    Offset    Description
##  (Bytes)  (Bytes)
##  ***Prefix***
##  ***CCD (command_id = WRITEMEM_CMD)***
##  8        0         64 bit register address
##  x        8         data
##                     Number of bytes to write to the remote device’s register map.
##  ***Postfix***
##	-------------------------------------------------------------------------------------
##	-------------------------------------------------------------------------------------
##  Table 12 - WriteMem Ack SCD-Fields
##
##  Width    Offset    Description
##  (Bytes)  (Bytes)
##  ***Prefix***
##  ***CCD-ACK (command_id = WRITEMEM_ACK)***
##  2        0         reserved
##                     This reserved field is only sent if the length_written field is sent with the
##                     acknowledge. If it is sent it is to be set to 0.
##  2        2         length written
##                     Number of bytes successfully written to the remote device’s register map.
##                     The length written field must only be sent if the according bit in the
##                     Device Capability register is set.
##  ***Postfix***
##	-------------------------------------------------------------------------------------




##	-------------------------------------------------------------------------------------
##	解析u3v leader命令
##	-------------------------------------------------------------------------------------
def u3vl_proc(*params) :
	##	===============================================================================================
	##	ref ***save parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	传入参数
	##	-------------------------------------------------------------------------------------
	debug	= params[0];
	first_byte_pos	= params[1];
	line_cnt		= params[2];
	file_content	= params[3];
	if(debug==1):	print("here is u3vl proc");

	##	===============================================================================================
	##	ref ***catch info from leader***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	bushound log 日志中，每一行只有4组数据，每一组数据宽度是13byte
	##	--13byte中，最后2个byte是空字符
	##	-------------------------------------------------------------------------------------
	line_content	= file_content[line_cnt];
	line_content	= line_content[first_byte_pos:first_byte_pos+13*4];
	if(debug==1):	print("here is u3vl proc,line_content is",line_content);

	##	-------------------------------------------------------------------------------------
	##	获得blockid
	##	-------------------------------------------------------------------------------------
	blockid	= line_content[48:50]+line_content[45:47]+line_content[42:44]+line_content[39:41]+line_content[35:37]+line_content[32:34]+line_content[29:31]+line_content[26:28];
	blockid	= int(blockid,16);
	blockid	= hex(blockid);
	blockid	= " block is "+blockid+'.';
	if(debug==1):	print("here is u3vl proc,blockid is ",blockid);

	##	-------------------------------------------------------------------------------------
	##	进入下一行
	##	-------------------------------------------------------------------------------------
	##	-------------------------------------------------------------------------------------
	##	如果已经是文件末尾，就不要再读了，直接返回空值
	##	-------------------------------------------------------------------------------------
	if(line_cnt==len(file_content)-1):
		ret	= [line_cnt,"data not enough"];
		return	ret;
	line_content	= file_content[line_cnt+1];
	line_content	= line_content[first_byte_pos:first_byte_pos+13*4];

	##	-------------------------------------------------------------------------------------
	##	获得chunk_mode_active
	##	-------------------------------------------------------------------------------------
	if(line_content[9:10]=='4'):
		chunk_mode_active	= '1';
	else:
		chunk_mode_active	= '0';
	chunk_mode_active	= " chunk_mode_active is "+chunk_mode_active+'.';

	##	-------------------------------------------------------------------------------------
	##	获得timestamp
	##	-------------------------------------------------------------------------------------
	timestamp	= line_content[35:37]+line_content[32:34]+line_content[29:31]+line_content[26:28]+line_content[22:24]+line_content[19:21]+line_content[16:18]+line_content[13:15];
	timestamp	= int(timestamp,16);
	timestamp	= hex(timestamp);
	timestamp	= " timestamp is "+timestamp+'.';
	if(debug==1):	print("here is u3vl proc,timestamp is ",timestamp);

	##	-------------------------------------------------------------------------------------
	##	获得 pixel format
	##	-------------------------------------------------------------------------------------
	pixel_format	= line_content[48:50]+line_content[45:47]+line_content[42:44]+line_content[39:41];
	pixel_format	= "0x"+pixel_format;
	pixel_format	= pixel_format_match(debug,pixel_format);
	pixel_format	= " pixel_format is "+pixel_format+'.';
	if(debug==1):	print("here is u3vl proc,pixel_format is ",pixel_format);

	##	-------------------------------------------------------------------------------------
	##	进入下一行
	##	-------------------------------------------------------------------------------------
	##	-------------------------------------------------------------------------------------
	##	如果已经是文件末尾，就不要再读了，直接返回空值
	##	-------------------------------------------------------------------------------------
	if(line_cnt==len(file_content)-2):
		ret	= [line_cnt,"data not enough"];
		return	ret;
	line_content	= file_content[line_cnt+2];
	line_content	= line_content[first_byte_pos:first_byte_pos+13*4];

	##	-------------------------------------------------------------------------------------
	##	获得 size_x
	##	-------------------------------------------------------------------------------------
	size_x		= line_content[3:5]+line_content[0:2];
	size_x_dec	= int(size_x,16);
	size_x_dec	= str(size_x_dec);
	size_x		= " size_x is 0x"+size_x+'('+size_x_dec+').';
	if(debug==1):	print("here is u3vl proc,size_x is ",size_x);

	##	-------------------------------------------------------------------------------------
	##	获得 size_y
	##	-------------------------------------------------------------------------------------
	size_y		= line_content[16:18]+line_content[13:15];
	size_y_dec	= int(size_y,16);
	size_y_dec	= str(size_y_dec);
	size_y		= " size_y is 0x"+size_y+'('+size_y_dec+').';
	if(debug==1):	print("here is u3vl proc,size_y is ",size_y);

	##	-------------------------------------------------------------------------------------
	##	获得 offset_x
	##	-------------------------------------------------------------------------------------
	offset_x		= line_content[29:31]+line_content[26:28];
	offset_x_dec	= int(offset_x,16);
	offset_x_dec	= str(offset_x_dec);
	offset_x		= " offset_x is 0x"+offset_x+'('+offset_x_dec+').';
	if(debug==1):	print("here is u3vl proc,offset_x is ",offset_x);

	##	-------------------------------------------------------------------------------------
	##	获得 size_y
	##	-------------------------------------------------------------------------------------
	offset_y		= line_content[42:44]+line_content[39:41];
	offset_y_dec	= int(offset_y,16);
	offset_y_dec	= str(offset_y_dec);
	offset_y		= " offset_y is 0x"+offset_y+'('+offset_y_dec+').';
	if(debug==1):	print("here is u3vl proc,offset_y is ",offset_y);

	##	===============================================================================================
	##	ref ***return***
	##	===============================================================================================
	ret	= [line_cnt,blockid+chunk_mode_active+timestamp+pixel_format+size_x+size_y+offset_x+offset_y];
	return	ret;


##	-------------------------------------------------------------------------------------
##	解析u3v trailer命令
##	-------------------------------------------------------------------------------------
def u3vt_proc(*params) :
	##	===============================================================================================
	##	ref ***save parameter***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	传入参数
	##	-------------------------------------------------------------------------------------
	debug			= params[0];
	first_byte_pos	= params[1];
	line_cnt		= params[2];
	file_content	= params[3];
	if(debug==1):	print("here is u3vt proc");

	##	===============================================================================================
	##	ref ***catch info from trailer***
	##	===============================================================================================
	##	-------------------------------------------------------------------------------------
	##	bushound log 日志中，每一行只有4组数据，每一组数据宽度是13byte
	##	--13byte中，最后2个byte是空字符
	##	-------------------------------------------------------------------------------------
	line_content	= file_content[line_cnt];
	line_content	= line_content[first_byte_pos:first_byte_pos+13*4];
	if(debug==1):	print("here is u3vt proc,line_content is",line_content);
	if(debug==1):	print("here is u3vt proc,line_cnt is",line_cnt);

	##	-------------------------------------------------------------------------------------
	##	获得 trailer_size
	##	-------------------------------------------------------------------------------------
	trailer_size	= line_content[19:21];
	trailer_size	= int(trailer_size,16);
	trailer_size	= str(trailer_size);
	trailer_size	= " trailer_size is "+trailer_size+'.';
	if(debug==1):	print("here is u3vt proc,trailer_size is ",trailer_size);

	##	-------------------------------------------------------------------------------------
	##	获得blockid
	##	-------------------------------------------------------------------------------------
	blockid	= line_content[48:50]+line_content[45:47]+line_content[42:44]+line_content[39:41]+line_content[35:37]+line_content[32:34]+line_content[29:31]+line_content[26:28];
	blockid	= int(blockid,16);
	blockid	= hex(blockid);
	blockid	= " block is "+blockid+'.';
	if(debug==1):	print("here is u3vt proc,blockid is ",blockid);

	##	-------------------------------------------------------------------------------------
	##	进入下一行
	##	-------------------------------------------------------------------------------------
	##	-------------------------------------------------------------------------------------
	##	如果已经是文件末尾，就不要再读了，直接返回空值
	##	-------------------------------------------------------------------------------------
	if(line_cnt==len(file_content)-1):
		ret	= [line_cnt,"data not enough"];
		return	ret;
	line_content	= file_content[line_cnt+1];
	line_content	= line_content[first_byte_pos:first_byte_pos+13*4];

	##	-------------------------------------------------------------------------------------
	##	获得 status
	##	-------------------------------------------------------------------------------------
	status	= line_content[3:5]+line_content[0:2];
	status	= " status is 0x"+status+'.';
	if(debug==1):	print("here is u3vt proc,status is ",status);

	##	-------------------------------------------------------------------------------------
	##	获得 valid_payload_size
	##	-------------------------------------------------------------------------------------
	valid_payload_size	= line_content[22:24]+line_content[19:21]+line_content[16:18]+line_content[13:15];
	valid_payload_size_dec	= int(valid_payload_size,16);
	valid_payload_size_dec	= str(valid_payload_size_dec);
	valid_payload_size		= " valid_payload_size is 0x"+valid_payload_size+'('+valid_payload_size_dec+').';
	if(debug==1):	print("here is u3vt proc,valid_payload_size is ",valid_payload_size);

	##	-------------------------------------------------------------------------------------
	##	获得 trailer_size_y
	##	-------------------------------------------------------------------------------------
	trailer_size_y		= line_content[42:44]+line_content[39:41];
	trailer_size_y_dec	= int(trailer_size_y,16);
	trailer_size_y_dec	= str(trailer_size_y_dec);
	trailer_size_y		= " trailer_size_y is 0x"+trailer_size_y+'('+trailer_size_y_dec+').';
	if(debug==1):	print("here is u3vt proc,trailer_size_y is ",trailer_size_y);

#	##	-------------------------------------------------------------------------------------
#	##	进入下一行
#	##	-------------------------------------------------------------------------------------
#	##	-------------------------------------------------------------------------------------
#	##	如果已经是文件末尾，就不要再读了，直接返回空值
#	##	-------------------------------------------------------------------------------------
#	if(line_cnt==len(file_content)-2):
#		ret	= [line_cnt,"data not enough"];
#		return	ret;
#	line_content	= file_content[line_cnt+2];
#	line_content	= line_content[first_byte_pos:first_byte_pos+13*4];
#
#	if(debug==1):	print("here is u3vt proc,line_content is",line_content);
#	if(debug==1):	print("here is u3vt proc,line_cnt is",line_cnt);
#
#	##	-------------------------------------------------------------------------------------
#	##	获得 chunk_layout_id
#	##	-------------------------------------------------------------------------------------
#	chunk_layout_id		= line_content[0:2];
#	chunk_layout_id_dec	= int(chunk_layout_id,16);
#	chunk_layout_id_dec	= str(chunk_layout_id_dec);
#	chunk_layout_id		= " chunk_layout_id is 0x"+chunk_layout_id+'('+chunk_layout_id_dec+').';
#	if(debug==1):	print("here is u3vt proc,chunk_layout_id is ",chunk_layout_id);

	##	===============================================================================================
	##	ref ***return***
	##	===============================================================================================
#	ret	= [line_cnt,trailer_size+blockid+status+valid_payload_size+trailer_size_y+chunk_layout_id];
	##	只解析 32 byte 的trailer 大小
	ret	= [line_cnt,trailer_size+blockid+status+valid_payload_size+trailer_size_y];
	return	ret;

def pixel_format_match(*params) :
	debug			= params[0];
	pixel_format	= params[1];

	if(pixel_format=="0x01010037"):		format_name	= "Mono1p" ;
	elif(pixel_format=="0x01020038"):	format_name	= "Mono2p" ;
	elif(pixel_format=="0x01040039"):	format_name	= "Mono4p" ;
	elif(pixel_format=="0x01080001"):	format_name	= "Mono8"  ;
	elif(pixel_format=="0x01100003"):	format_name	= "Mono10" ;
	elif(pixel_format=="0x010a0046"):	format_name	= "Mono10p";
	elif(pixel_format=="0x01100005"):	format_name	= "Mono12" ;
	elif(pixel_format=="0x010c0047"):	format_name	= "Mono12p";
	elif(pixel_format=="0x01100025"):	format_name	= "Mono14" ;
	elif(pixel_format=="0x01100007"):	format_name	= "Mono16" ;
	elif(pixel_format=="0x01080008"):	format_name	= "BayerGR8"  ;
	elif(pixel_format=="0x0110000C"):	format_name	= "BayerGR10" ;
	elif(pixel_format=="0x010A0056"):	format_name	= "BayerGR10p";
	elif(pixel_format=="0x01100010"):	format_name	= "BayerGR12" ;
	elif(pixel_format=="0x010C0057"):	format_name	= "BayerGR12p";
	elif(pixel_format=="0x0110002E"):	format_name	= "BayerGR16" ;
	elif(pixel_format=="0x01080009"):	format_name	= "BayerRG8"  ;
	elif(pixel_format=="0x0110000D"):	format_name	= "BayerRG10" ;
	elif(pixel_format=="0x010A0058"):	format_name	= "BayerRG10p";
	elif(pixel_format=="0x01100011"):	format_name	= "BayerRG12" ;
	elif(pixel_format=="0x010C0059"):	format_name	= "BayerRG12p";
	elif(pixel_format=="0x0110002F"):	format_name	= "BayerRG16" ;
	elif(pixel_format=="0x0108000A"):	format_name	= "BayerGB8"  ;
	elif(pixel_format=="0x0110000E"):	format_name	= "BayerGB10" ;
	elif(pixel_format=="0x010A0054"):	format_name	= "BayerGB10p";
	elif(pixel_format=="0x01100012"):	format_name	= "BayerGB12" ;
	elif(pixel_format=="0x010C0055"):	format_name	= "BayerGB12p";
	elif(pixel_format=="0x01100030"):	format_name	= "BayerGB16" ;
	elif(pixel_format=="0x0108000B"):	format_name	= "BayerBG8"  ;
	elif(pixel_format=="0x0110000F"):	format_name	= "BayerBG10" ;
	elif(pixel_format=="0x010A0052"):	format_name	= "BayerBG10p";
	elif(pixel_format=="0x01100013"):	format_name	= "BayerBG12" ;
	elif(pixel_format=="0x010C0053"):	format_name	= "BayerBG12p";
	elif(pixel_format=="0x01100031"):	format_name	= "BayerBG16" ;
	elif(pixel_format=="0x02180015"):	format_name	= "BGR8"      ;
	elif(pixel_format=="0x02300019"):	format_name	= "BGR10"     ;
	elif(pixel_format=="0x021E0048"):	format_name	= "BGR10p"    ;
	elif(pixel_format=="0x0230001B"):	format_name	= "BGR12"     ;
	elif(pixel_format=="0x02240049"):	format_name	= "BGR12p"    ;
	elif(pixel_format=="0x0230004A"):	format_name	= "BGR14"     ;
	elif(pixel_format=="0x0230004B"):	format_name	= "BGR16"     ;
	elif(pixel_format=="0x02200017"):	format_name	= "BGRa8"     ;
	elif(pixel_format=="0x0240004C"):	format_name	= "BGRa10"    ;
	elif(pixel_format=="0x0228004D"):	format_name	= "BGRa10p"   ;
	elif(pixel_format=="0x0240004E"):	format_name	= "BGRa12"    ;
	elif(pixel_format=="0x0230004F"):	format_name	= "BGRa12p"   ;
	elif(pixel_format=="0x02400050"):	format_name	= "BGRa14"    ;
	elif(pixel_format=="0x02400051"):	format_name	= "BGRa16"    ;
	elif(pixel_format=="0x0218005B"):	format_name	= "YCbCr8"    ;
	elif(pixel_format=="0x0210003B"):	format_name	= "YCbCr422_8";
	elif(pixel_format=="0x020C005A"):	format_name	= "YCbCr411_8";

	else:	format_name	= "Unkown PixelFormat";

	return	pixel_format+'('+format_name+')';

	##	-------------------------------------------------------------------------------------
	##	USB3 Vision 	version 1.0.1	March, 2015
	##	table 5-14: Recommended Pixel Formats
	##
	##	Mono1p			0x01010037
	##	Mono2p			0x01020038
	##	Mono4p			0x01040039
	##	Mono8			0x01080001
	##	Mono10			0x01100003
	##	Mono10p			0x010a0046
	##	Mono12			0x01100005
	##	Mono12p			0x010c0047
	##	Mono14			0x01100025
	##	Mono16			0x01100007
	##
	##	BayerGR8		0x01080008
	##	BayerGR10		0x0110000C
	##	BayerGR10p		0x010A0056
	##	BayerGR12		0x01100010
	##	BayerGR12p		0x010C0057
	##	BayerGR16		0x0110002E
	##
	##	BayerRG8		0x01080009
	##	BayerRG10		0x0110000D
	##	BayerRG10p		0x010A0058
	##	BayerRG12		0x01100011
	##	BayerRG12p		0x010C0059
	##	BayerRG16		0x0110002F
	##
	##	BayerGB8		0x0108000A
	##	BayerGB10		0x0110000E
	##	BayerGB10p		0x010A0054
	##	BayerGB12		0x01100012
	##	BayerGB12p		0x010C0055
	##	BayerGB16		0x01100030
	##
	##	BayerBG8		0x0108000B
	##	BayerBG10		0x0110000F
	##	BayerBG10p		0x010A0052
	##	BayerBG12		0x01100013
	##	BayerBG12p		0x010C0053
	##	BayerBG16		0x01100031
    ##
	##	BGR8			0x02180015
	##	BGR10			0x02300019
	##	BGR10p			0x021E0048
	##	BGR12			0x0230001B
	##	BGR12p			0x02240049
	##	BGR14			0x0230004A
	##	BGR16			0x0230004B
    ##
	##	BGRa8			0x02200017
	##	BGRa10			0x0240004C
	##	BGRa10p			0x0228004D
	##	BGRa12			0x0240004E
	##	BGRa12p			0x0230004F
	##	BGRa14			0x02400050
	##	BGRa16			0x02400051
	##
	##	YCbCr8			0x0218005B
	##	YCbCr422_8		0x0210003B
	##	YCbCr411_8		0x020C005A
	##  -------------------------------------------------------------------------------------