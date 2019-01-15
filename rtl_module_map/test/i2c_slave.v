//   ==================================================================
//   >>>>>>>>>>>>>>>>>>>>>>> COPYRIGHT NOTICE <<<<<<<<<<<<<<<<<<<<<<<<<
//   ------------------------------------------------------------------
//   Copyright (c) 2013 by Lattice Semiconductor Corporation
//   ALL RIGHTS RESERVED
//   ------------------------------------------------------------------
//
//   Permission:
//
//      Lattice SG Pte. Ltd. grants permission to use this code
//      pursuant to the terms of the Lattice Reference Design License Agreement.
//
//
//   Disclaimer:
//
//      This VHDL or Verilog source code is intended as a design reference
//      which illustrates how these types of functions can be implemented.
//      It is the user's responsibility to verify their design for
//      consistency and functionality through the use of formal
//      verification methods.  Lattice provides no warranty
//      regarding the use or functionality of this code.
//
//   --------------------------------------------------------------------
//
//                  Lattice SG Pte. Ltd.
//                  101 Thomson Road, United Square #07-02
//                  Singapore 307591
//
//
//                  TEL: 1-800-Lattice (USA and Canada)
//                       +65-6631-2000 (Singapore)
//                       +1-503-268-8001 (other locations)
//
//                  web: http://www.latticesemi.com/
//                  email: techsupport@latticesemi.com
//
//   --------------------------------------------------------------------
//


//
//
//  Name:  i2c_slave.v
//
//  Description: Generic i2c slave module with 1 bidirectional data port
// 		 1.supports random write, random read, sequential read
// 		 and burst write / read
//
//-------------------------------------------------------------------------
// Code Revision History :
//-------------------------------------------------------------------------
// Ver: | Author	|Mod. Date	|Changes Made:
// V1.0 | cm		|8/2005     |Init ver
// V1.1 | ks		|1/2007		|change slave address to be input
// V1.2 | cm		|6/2009		|change slave address back to parameter
//                              |emulate slave is not ready (clk stretch)
// V1.3 | cm,cwd    |7/4/10     |added delay element to scl to prevent false
//                              |start due to trace delays
//-------------------------------------------------------------------------

`timescale 1ns/1ps

module i2c_slave (XRESET, ready, start, stop, data_in, data_out, r_w, data_vld, scl_in, scl_oe, sda_in, sda_oe);

	// generic ports
	input        XRESET; 		                                       // System Reset
	input 	     ready; 						       // back end system ready signal
	//input  [6:0] I2C_SLAVE_ADDR;                                         // I2C addr from regmap
	input  [7:0] data_in; 	                                               // parallel data in
	output [7:0] data_out; 	                                               // parallel data out
	output       r_w;                                                      // read/write signal to the reg_map bloc
	output       data_vld;		                                       // data valid from i2c
	output       start;                                                    // start of the i2c cycle
	output       stop;					               // stop the i2c cycle

	// i2c ports
	input        scl_in;						       // SCL clock line
	output 	     scl_oe;
	input        sda_in;		                                       // i2c serial data line in
	output       sda_oe;                                                   // controls sda output enable


	/*****************************************
	Define states of the state machine
	*****************************************/

	parameter I2C_SLAVE_ADDR = 7'b1000010;
	//parameter I2C_SLAVE_ADDR = 7'b1000001;

	parameter idle=5'h0, addr7=5'h1, addr6=5'h2, addr5=5'h3,
	addr4=5'h4, addr3=5'h5, addr2=5'h6, addr1=5'h7,
	det_rw=5'h8, ack=5'h9, data7=5'ha, data6=5'hb,
	data5=5'hc, data4=5'hd, data3=5'he, data2=5'hf,
	data1=5'h10, data0=5'h11;

	reg [7:0] data_int;                                                    // internal data register
	reg start, stop;				                       // start and stop detection of I2C cycles
	reg [4:0] sm_state; 				                       // state machine
	reg [7:0] shift;				                       // shift register attached to I2C controller
	reg r_w;		 			                       // indicate read/write operation
	reg ack_out;					                       // acknowledge output from slave to master
	reg sda_en;	      			                               // OE control of sda signal, could use open drain feature
	reg vld_plse;		       	                                       // data valid pulse

	wire start_rst;				                               // reset signals for START and STOP bits


	// synthesis translate_off
	reg		[127:0]			state_ascii;
	always @ ( * ) begin
		case(sm_state)
			5'd0 	:	state_ascii	= "idle";
			5'd1 	:	state_ascii	= "addr7";
			5'd2 	:	state_ascii	= "addr6";
			5'd3 	:	state_ascii	= "addr5";
			5'd4 	:	state_ascii	= "addr4";
			5'd5 	:	state_ascii	= "addr3";
			5'd6 	:	state_ascii	= "addr2";
			5'd7 	:	state_ascii	= "addr1";
			5'd8 	:	state_ascii	= "det_rw";
			5'd9 	:	state_ascii	= "ack";
			5'd10 	:	state_ascii	= "data7";
			5'd11 	:	state_ascii	= "data6";
			5'd12 	:	state_ascii	= "data5";
			5'd13 	:	state_ascii	= "data4";
			5'd14 	:	state_ascii	= "data3";
			5'd15 	:	state_ascii	= "data2";
			5'd16 	:	state_ascii	= "data1";
			5'd17 	:	state_ascii	= "data0";
			default	:	state_ascii	= "ERROR";
		endcase
	end
	// synthesis translate_on




	/*****************************************
	Generate reset signals for start and stop
	*****************************************/
	assign start_rst = ((sm_state == addr7))? 1'b1 : 1'b0;                 // used to reset the start register after we move to addr7
	wire start_async_rst = start_rst | XRESET;                             // oring the reset signal external and internal
	wire stop_async_rst = start | XRESET;                                  // same for stop reset

	/*****************************************
	register to delay SDA
	prevents false start/re-starts from syncronized
	falling edges (sda and scl)
	******************************************/
	reg sda_f;
	wire #1 sda_clk;
	xor u1 (sda_clk, sda_f, sda_in);                                       // generate a narrow pulse based on the delay between sda_in and sda_f

	always @ (posedge sda_clk or posedge start_async_rst)		       // use the narrow clock pulse to delay sda_in through a register
	begin
		if (start_async_rst)
		begin
			if(sda_in)
			sda_f = #1 1'b1;
			else
			sda_f = #1 1'b0;
		end
		else
		sda_f = #1 sda_in;
	end

	/*****************************************
	Detect I2C Cycle Start
	*****************************************/
	always @ (negedge sda_f or posedge start_async_rst)	               // use delayed version of sda_in to prevent the false START
	begin
		if (start_async_rst)
		start = #1 1'b0;
		else
		start = #1 scl_in;
	end

	/*****************************************
	Detect I2C Cycle Stop
	*****************************************/
	always @(posedge sda_in or posedge stop_async_rst)
	begin
		if (stop_async_rst)
		stop = #1 1'b0;
		else
		stop = #1 scl_in;
	end


	/*****************************************
	FSM check the addr byte and track rw opp
	*****************************************/

	always @(posedge scl_in or posedge XRESET) begin
		if (XRESET) begin
			sm_state <=  idle;                                                 // reset fsm to idle
			r_w      <=  1'b1;				                   // initial value for read
			vld_plse <=  1'b0;
		end
		else begin
			case (sm_state)
				idle : begin
					vld_plse <=  1'b0;
					if (start) begin				           // start the I2C addr cycle
						sm_state <=  addr7;
					end
					else if (stop) begin                                     // stop and go to idle
						sm_state <=  idle;
					end
					else begin
						sm_state <=  idle;
					end
				end
				addr7: 	begin
					if (shift[0] == I2C_SLAVE_ADDR[6]) begin	           // checking the slave addr
						sm_state <=  addr6;
					end
					else begin
						sm_state <=  idle;
					end
				end
				addr6: begin
					if (shift[0] == I2C_SLAVE_ADDR[5]) begin
						sm_state <=  addr5;
					end

					else begin
						sm_state <=  idle;
					end
				end
				addr5: begin
					if (shift[0] == I2C_SLAVE_ADDR[4]) begin
						sm_state <=  addr4;
					end

					else begin
						sm_state <=  idle;
					end
				end
				addr4: begin
					if (shift[0] == I2C_SLAVE_ADDR[3]) begin
						sm_state <=  addr3;
					end
					else begin
						sm_state <=  idle;
					end
				end
				addr3: begin
					if (shift[0] == I2C_SLAVE_ADDR[2]) begin
						sm_state <=  addr2;
					end
					else begin
						sm_state <=  idle;
					end
				end
				addr2: begin
					if (shift[0] == I2C_SLAVE_ADDR[1]) begin
						sm_state <=  addr1;
					end
					else begin
						sm_state <=  idle;
					end
				end
				addr1: begin
					if (shift[0] == I2C_SLAVE_ADDR[0]) begin
						sm_state <=  det_rw;
						r_w      <=  sda_in;		           // store the read / write direction bit
					end
					else begin
						sm_state <=  idle;
					end
				end
				det_rw: begin
					sm_state <=  ack;
				end
				ack   :	begin
					if (ready) begin
						sm_state <=  data7;
						vld_plse <=  1'b0;
					end
					else begin
						sm_state <= idle;
						vld_plse <= 1'b0;
					end
				end
				data7 : begin
					if (stop) begin
						sm_state <= idle;		           // detect stop signal from Master
					end

					else if (start) begin
						sm_state <= addr7;           // detect RESTART signal from Master
					end
					else begin
						sm_state <= data6;
					end
				end
				data6 :	sm_state <=  data5;
				data5 :	sm_state <=  data4;
				data4 :	sm_state <=  data3;
				data3 :	sm_state <=  data2;
				data2 :	sm_state <=  data1;
				data1 :	begin
					sm_state <=  data0;
					vld_plse <= 1'b1;
				end
				data0 :	begin
					vld_plse <= 1'b0;			     // detect repeated read, write or read/write
					if (!sda_in) begin	// 0 means acknowledged
						sm_state <= ack;
					end
					else begin
						sm_state <= idle;                                        // 1 means not-acknowledged if slave or Master wants to stop
					end
				end
				default:     sm_state <= idle;                                   // default state
			endcase
		end
	end

	/********************************************
	Read cycle (slave trasmit, master receive)
	Write Cycle (slave receive, master transmit)
	Slave generate ACKOUT during write cycle
	********************************************/

	always @(negedge scl_in or posedge XRESET)
	begin	 					                                       // data should be ready on SDA line when SCL is high
		if (XRESET) begin
			ack_out <= #1 0;
		end
		else if (sm_state == det_rw) begin
			ack_out <= #1 1'b1;
		end
		else if (sm_state == data0) begin
			if (!r_w) begin			                                               // if slave is rx, acknowledge after successful receive
				ack_out <= #1 1'b1;
			end
			else begin			                               // if slave is tx, acknowledge comes from Master
				ack_out <= #1 1'b0;
			end
		end
		else begin
			ack_out <= #1 1'b0;
		end
	end


	/********************************************
	Enable starting from ACK state
	********************************************/

	always @(negedge scl_in or posedge XRESET) begin
		if (XRESET) begin
			sda_en <= 0;
		end
		else if (r_w && (sm_state == ack)) begin
			sda_en <= #1 !data_in[7];
		end
		else if (r_w && ((sm_state > ack) && (sm_state < data0))) begin
			sda_en <= #1 ~shift[6];
		end
		else begin
			sda_en <= #1 0;
		end
	end

	/********************************************
	SDA OE cntr gen '1' will pull the line low
	********************************************/

	assign sda_oe = ((ack_out == 1'b1) | (sda_en == 1'b1));                                // sda_out is logic '0' at the top level
	// sda_oe cntrl sda_out at top level

	assign scl_oe = (sm_state == ack) & (~ready);					       // if scl_oe = 1, then scl is pulled down

	/*******************************
	Shift operation for READ data
	*******************************/

	always @(negedge scl_in or posedge XRESET)
	begin
		if (XRESET) begin                                                                    // Reset added to make it work
			shift <= #1 8'b0;
		end
		else begin
			if ((sm_state == idle) && (start)) begin
				shift[0] <= #1 sda_in;
			end
			else if ((sm_state >= addr7) && (sm_state <= addr1)) begin
				shift[0] <= #1 sda_in;
			end
			else if (r_w && (sm_state == ack)) begin   	                               // 2nd version
				shift <= #1 data_in;	    			               // load the GPIO data into shift registers
			end
			else if ((sm_state > ack) && (sm_state <=data0))                       // start shift the data out to SDA line
			begin						                                                 // 2nd version
				shift[7:1] <= #1 shift[6:0];
				shift[0]   <= #1 sda_in;
			end
		end

	end

	/********************************************
	data output register
	********************************************/

	always @ (posedge scl_in or posedge XRESET)
	begin
		if (XRESET) begin
			data_int <=  #1 8'h0;
		end
		else if (!r_w && ack_out && vld_plse) begin
			data_int <=  #1 shift;
		end
	end

	assign data_out = data_int;
	assign data_vld = vld_plse;

endmodule

//--------------------------------EOF-----------------------------------------
