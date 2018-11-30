//-------------------------------------------------------------------------------------------------
//  -- ��Ȩ������   : �й���㣨���ţ����޹�˾����ͼ���Ӿ������ֹ�˾, 2010 -2015.
//  -- ���ܼ���     ������.
//  -- ����         : Ӳ������FPGA������
//  -- ģ����       : clk_gen
//  -- �����       : �Ϻ���
//-------------------------------------------------------------------------------------------------
//
//  -- �汾��¼ :
//
//  -- ����         :| �޸�����				:|  �޸�˵��
//-------------------------------------------------------------------------------------------------
//  -- �Ϻ���       :| 2016/12/14 13:37:15	:|  ��ʼ�汾
//-------------------------------------------------------------------------------------------------
//
//  -- ģ������     :
//              1)  :
//
//              2)  :
//
//              3)  :
//
//-------------------------------------------------------------------------------------------------
//`include			"clk_gen_def.v"
//���浥λ/����
`timescale 1ns/1ps
//-------------------------------------------------------------------------------------------------

module driver_fb_read_init_pdiv (
	input											clk
	);

	//	ref parameters
	parameter	BID_WD						= driver.param.BID_WD	;
	parameter	PID_WD						= driver.param.PID_WD	;
	parameter	PTR_WD						= driver.param.PTR_WD	;
	parameter	SHORT_REG_WD				= driver.param.SHORT_REG_WD	;
	parameter	REG_WD						= driver.param.REG_WD	;
	parameter	LONG_REG_WD					= driver.param.LONG_REG_WD	;
	parameter	FRAME_BYTE_ADDR_WD			= driver.param.FRAME_BYTE_ADDR_WD	;
	parameter	PKT_LENGTH_WD				= driver.param.PKT_LENGTH_WD	;
	parameter	PKT_CNT_WD					= driver.param.PKT_CNT_WD	;

	parameter	STATIS_VALID				= driver.param.STATIS_VALID			    ;
	parameter	INFO_WAIT_TIME				= driver.param.INFO_WAIT_TIME			;
	parameter	IMAGE_WAIT_TIME				= driver.param.IMAGE_WAIT_TIME			;
	parameter	STATIS_WAIT_TIME			= driver.param.STATIS_WAIT_TIME		    ;
	parameter	FVAL_FALL_WAIT_TIME			= driver.param.FVAL_FALL_WAIT_TIME		;
	parameter	BID_INIT_VALUE				= driver.param.BID_INIT_VALUE			;
	parameter	INFO_SIZE					= driver.param.INFO_SIZE				;
	parameter	STATIS_SIZE					= driver.param.STATIS_SIZE				;
	parameter	MROI_MAX_NUM 				= driver.param.MROI_MAX_NUM 			;
	parameter	DATA_WD						= driver.param.DATA_WD					;
	parameter	MROI_OFFSET_WD				= driver.param.MROI_OFFSET_WD			;
	parameter	MROI_IMAGE_SIZE_WD			= driver.param.MROI_IMAGE_SIZE_WD		;

	//	ref signals
	wire										i_fval_pdiv						;
	wire										i_pval							;
	wire										i_aval							= 'b0;
	reg											i_info_flag						= 'b0;
	reg											i_image_flag					= 'b0;
	reg											i_statis_flag					= 'b0;
	reg		[FRAME_BYTE_ADDR_WD-1:0]			iv_rd_addr						= 'b0;
	reg		[FRAME_BYTE_ADDR_WD-1:0]			iv_rd_length					= 'b0;

	reg		[15:0]								iv_width					= 16'd16	;
	reg		[15:0]								iv_line_hide				= 16'd10	;
	reg		[15:0]								iv_height					= 16'd16	;
	reg		[15:0]								iv_frame_hide				= 16'd5		;
	reg		[15:0]								iv_front_porch				= 16'd4		;
	reg		[15:0]								iv_back_porch				= 16'd3		;

	reg		[LONG_REG_WD-1:0]					iv_timestamp					= 'b0	;
	reg		[LONG_REG_WD-1:0]					iv_frame_interval				= 'b0	;
	reg		[REG_WD-1:0]						iv_pixel_format					= 'b0	;
	reg		[MROI_OFFSET_WD-1:0]				iv_single_roi_offset_x			= 'b0	;
	reg		[MROI_OFFSET_WD-1:0]				iv_single_roi_offset_y			= 'b0	;
	reg		[MROI_OFFSET_WD-1:0]				iv_single_roi_width				= 'b0	;
	reg		[MROI_OFFSET_WD-1:0]				iv_single_roi_height			= 'b0	;
	reg		[MROI_IMAGE_SIZE_WD-1:0]			iv_single_roi_image_size		= 'b0	;
	reg		[MROI_IMAGE_SIZE_WD-1:0]			iv_single_roi_payload_size		= 'b0	;
	reg											i_chunk_mode_active				= 1'b0	;
	reg											i_chunkid_en_img				= 1'b0	;
	reg											i_chunkid_en_fid				= 1'b0	;
	reg											i_chunkid_en_ts					= 1'b0	;
	reg											i_chunkid_en_fint				= 1'b0	;
	reg		[LONG_REG_WD-1:0]					iv_expect_payload_size			= 'b0	;
	reg											i_mroi_global_en				= 1'b0	;
	reg		[REG_WD-1:0]						iv_mroi_single_en				= 'b0	;

	wire										w_fval_pattern	;
	wire										w_lval_pattern	;
	wire										w_fval_add	;
	wire										w_dval_add	;
	wire										w_info_flag_add	;
	wire										w_image_flag_add	;
	wire										w_statis_flag_add	;

	wire										o_fval_pdiv	;
	wire										o_pval_pdiv	;
	wire										o_aval_pdiv	;
	wire										o_info_flag_pdiv	;
	wire										o_image_flag_pdiv	;
	wire										o_statis_flag_pdiv	;
	wire	[FRAME_BYTE_ADDR_WD-1:0]			ov_rd_addr_pdiv	;
	wire	[FRAME_BYTE_ADDR_WD-1:0]			ov_rd_length_pdiv	;


	//	ref ARCHITECTURE

	//	-------------------------------------------------------------------------------------
	//	��������
	//	1.����ǵ�bit�źţ�����Ҫ���������ͨ��β׺ _on _off ������
	//	2.����Ƕ�bit�źţ�����Ҫ���������ǰ׺�� set_
	//	3.һ������£��ź������ֲ��䲻��д��������ź���������д
	//	4.�����һ��Ĵ������ã�ǰ׺�� cfg_������������п���
	//	-------------------------------------------------------------------------------------
	//  -------------------------------------------------------------------------------------
	//	--ref sensor pattern
	//  -------------------------------------------------------------------------------------
	task cfg_pattern_2para;
		input	[15:0]		width_input;
		input	[15:0]		height_input;
		begin
			#200
			iv_width			= width_input	;
			iv_line_hide		= 16'd10		;
			iv_height			= height_input	;
			iv_front_porch		= iv_line_hide/2		;
			iv_back_porch		= iv_line_hide/2		;
			iv_frame_hide		= 10'd1	;
		end
	endtask

	task cfg_pattern_5para;
		input	[15:0]				width_input			;
		input	[15:0]				line_hide_input		;
		input	[15:0]				height_input		;
		input	[15:0]				frame_hide_input	;
		input	[15:0]				porch_input			;
		begin
			#200
			iv_width			= width_input		;
			iv_line_hide		= line_hide_input	;
			iv_height			= height_input		;
			iv_frame_hide		= frame_hide_input	;
			iv_front_porch		= porch_input		;
			iv_back_porch		= 2		;
		end
	endtask

	frame_line_pattern_master # (
	.FVAL_LVAL_ALIGN		("FALSE"		),
	.DUMMY_LINE_FRONT		(1				),
	.DUMMY_LINE_BACK		(1				),
	.BLACK_LINE_FRONT		(1				),
	.BLACK_LINE_BACK		(1				)
	)
	frame_line_pattern_master_inst (
	.clk					(clk					),
	.reset					(1'b0					),
	.i_pause_en				(1'b0					),
	.i_continue_lval		(1'b0					),
	.iv_width				(iv_width				),
	.iv_line_hide			(iv_line_hide			),
	.iv_height				(iv_height				),
	.iv_frame_hide			(iv_frame_hide			),
	.iv_front_porch			(iv_front_porch			),
	.iv_back_porch			(iv_back_porch			),
	.o_fval					(w_fval_pattern			),
	.o_lval					(w_lval_pattern			)
	);

	frame_info_add # (
	.STATIS_VALID					(STATIS_VALID					),
	.INFO_WAIT_TIME					(INFO_WAIT_TIME					),
	.IMAGE_WAIT_TIME				(IMAGE_WAIT_TIME				),
	.STATIS_WAIT_TIME				(STATIS_WAIT_TIME				),
	.FVAL_FALL_WAIT_TIME			(FVAL_FALL_WAIT_TIME			),
	.BID_INIT_VALUE					(BID_INIT_VALUE					),
	.INFO_SIZE						(INFO_SIZE						),
	.STATIS_SIZE					(STATIS_SIZE					),
	.MROI_MAX_NUM					(MROI_MAX_NUM					),
	.DATA_WD						(DATA_WD						),
	.MROI_OFFSET_WD					(MROI_OFFSET_WD					),
	.MROI_IMAGE_SIZE_WD				(MROI_IMAGE_SIZE_WD				),
	.SHORT_REG_WD					(SHORT_REG_WD					),
	.REG_WD							(REG_WD							),
	.LONG_REG_WD					(LONG_REG_WD					)
	)
	frame_info_add_inst (
	.clk							(clk							),
	.reset							(1'b0							),
	.i_fval							(w_fval_pattern					),
	.i_dval							(w_lval_pattern					),
	.iv_pix_data					(256'b0							),
	.i_stream_enable				(driver.param.i_stream_enable	),
	.i_mroi_global_en				(i_mroi_global_en				),
	.iv_mroi_single_en				(iv_mroi_single_en				),
	.o_fval							(w_fval_add						),
	.o_dval							(w_dval_add						),
	.o_info_flag					(w_info_flag_add				),
	.o_image_flag					(w_image_flag_add				),
	.o_statis_flag					(w_statis_flag_add				),
	.ov_data						(								),
	.iv_timestamp					(iv_timestamp					),
	.iv_frame_interval				(iv_frame_interval				),
	.iv_pixel_format				(iv_pixel_format				),
	.iv_single_roi_offset_x			(iv_single_roi_offset_x			),
	.iv_single_roi_offset_y			(iv_single_roi_offset_y			),
	.iv_single_roi_width			(iv_single_roi_width			),
	.iv_single_roi_height			(iv_single_roi_height			),
	.iv_single_roi_image_size		(iv_single_roi_image_size		),
	.iv_single_roi_payload_size		(iv_single_roi_payload_size		),
	.i_chunk_mode_active			(i_chunk_mode_active			),
	.i_chunkid_en_img				(i_chunkid_en_img				),
	.i_chunkid_en_fid				(i_chunkid_en_fid				),
	.i_chunkid_en_ts				(i_chunkid_en_ts				),
	.i_chunkid_en_fint				(i_chunkid_en_fint				),
	.iv_expect_payload_size			(iv_expect_payload_size			)
	);

	fb_packet_divide # (
	.FRAME_BYTE_ADDR_WD		(FRAME_BYTE_ADDR_WD		),
	.PKT_LENGTH_WD			(PKT_LENGTH_WD			)
	)
	fb_packet_divide_inst (
	.clk					(clk					),
	.reset					(1'b0					),
	.iv_pkt_length			(driver.register.iv_pkt_length		),
	.o_ardy					(						),
	.i_fval					(w_fval_add				),
	.i_aval					(w_dval_add				),
	.i_info_flag			(w_info_flag_add		),
	.i_image_flag			(w_image_flag_add		),
	.i_statis_flag			(w_statis_flag_add		),
	.iv_rd_addr				(0						),
	.iv_rd_length			(256					),
	.i_ardy					(1'b1					),
	.o_fval					(o_fval_pdiv			),
	.o_pval					(o_pval_pdiv			),
	.o_aval					(o_aval_pdiv			),
	.o_info_flag			(o_info_flag_pdiv		),
	.o_image_flag			(o_image_flag_pdiv		),
	.o_statis_flag			(o_statis_flag_pdiv		),
	.ov_rd_addr				(ov_rd_addr_pdiv		),
	.ov_rd_length			(ov_rd_length_pdiv		)
	);




endmodule
