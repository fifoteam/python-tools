	always @ (posedge clk) begin
		piblic_timestamp_cnt	<= piblic_timestamp_cnt + 1'b1;
	end

	always @ (posedge clk) begin
		if(reset) begin
			timestamp_cnt_latch		<=	1'h0;
		end
		else if(i_wr_en && (iv_addr == 8'h51)) begin
			timestamp_cnt_latch	<=	iv_wr_data[1]	;
		end
		else begin
			timestamp_cnt_latch		<= 	1'h0;
		end
	end