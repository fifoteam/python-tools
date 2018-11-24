// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.1 (win64) Build 2188600 Wed Apr  4 18:40:38 MDT 2018
// Date        : Thu Nov 22 15:10:32 2018
// Host        : xht-PC running 64-bit Service Pack 1  (build 7601)
// Command     : write_verilog -force -mode funcsim
//               f:/DAHENG/hw_mars/branches/xinghaitao/mars_platform/develop_stage/fpga_module/fb_resend_ctrl/src/resend_mult/resend_mult/resend_mult_sim_netlist.v
// Design      : resend_mult
// Purpose     : This verilog netlist is a functional simulation representation of the design and should not be modified
//               or synthesized. This netlist cannot be used for SDF annotated simulation.
// Device      : xc7a100tfgg484-2
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* CHECK_LICENSE_TYPE = "resend_mult,mult_gen_v12_0_14,{}" *) (* downgradeipidentifiedwarnings = "yes" *) (* x_core_info = "mult_gen_v12_0_14,Vivado 2018.1" *) 
(* NotValidForBitStream *)
module resend_mult
   (CLK,
    A,
    B,
    CE,
    SCLR,
    P);
  (* x_interface_info = "xilinx.com:signal:clock:1.0 clk_intf CLK" *) (* x_interface_parameter = "XIL_INTERFACENAME clk_intf, ASSOCIATED_BUSIF p_intf:b_intf:a_intf, ASSOCIATED_RESET sclr, ASSOCIATED_CLKEN ce, FREQ_HZ 10000000, PHASE 0.000" *) input CLK;
  (* x_interface_info = "xilinx.com:signal:data:1.0 a_intf DATA" *) (* x_interface_parameter = "XIL_INTERFACENAME a_intf, LAYERED_METADATA undef" *) input [23:0]A;
  (* x_interface_info = "xilinx.com:signal:data:1.0 b_intf DATA" *) (* x_interface_parameter = "XIL_INTERFACENAME b_intf, LAYERED_METADATA undef" *) input [15:0]B;
  (* x_interface_info = "xilinx.com:signal:clockenable:1.0 ce_intf CE" *) (* x_interface_parameter = "XIL_INTERFACENAME ce_intf, POLARITY ACTIVE_LOW" *) input CE;
  (* x_interface_info = "xilinx.com:signal:reset:1.0 sclr_intf RST" *) (* x_interface_parameter = "XIL_INTERFACENAME sclr_intf, POLARITY ACTIVE_HIGH" *) input SCLR;
  (* x_interface_info = "xilinx.com:signal:data:1.0 p_intf DATA" *) (* x_interface_parameter = "XIL_INTERFACENAME p_intf, LAYERED_METADATA undef" *) output [39:0]P;

  wire [23:0]A;
  wire [15:0]B;
  wire CE;
  wire CLK;
  wire [39:0]P;
  wire SCLR;
  wire [47:0]NLW_U0_PCASC_UNCONNECTED;
  wire [1:0]NLW_U0_ZERO_DETECT_UNCONNECTED;

  (* C_A_TYPE = "1" *) 
  (* C_A_WIDTH = "24" *) 
  (* C_B_TYPE = "1" *) 
  (* C_B_VALUE = "10000001" *) 
  (* C_B_WIDTH = "16" *) 
  (* C_CCM_IMP = "0" *) 
  (* C_CE_OVERRIDES_SCLR = "0" *) 
  (* C_HAS_CE = "1" *) 
  (* C_HAS_SCLR = "1" *) 
  (* C_HAS_ZERO_DETECT = "0" *) 
  (* C_LATENCY = "1" *) 
  (* C_MODEL_TYPE = "0" *) 
  (* C_MULT_TYPE = "1" *) 
  (* C_OPTIMIZE_GOAL = "1" *) 
  (* C_OUT_HIGH = "39" *) 
  (* C_OUT_LOW = "0" *) 
  (* C_ROUND_OUTPUT = "0" *) 
  (* C_ROUND_PT = "0" *) 
  (* C_VERBOSITY = "0" *) 
  (* C_XDEVICEFAMILY = "artix7" *) 
  (* downgradeipidentifiedwarnings = "yes" *) 
  resend_mult_mult_gen_v12_0_14 U0
       (.A(A),
        .B(B),
        .CE(CE),
        .CLK(CLK),
        .P(P),
        .PCASC(NLW_U0_PCASC_UNCONNECTED[47:0]),
        .SCLR(SCLR),
        .ZERO_DETECT(NLW_U0_ZERO_DETECT_UNCONNECTED[1:0]));
endmodule

(* C_A_TYPE = "1" *) (* C_A_WIDTH = "24" *) (* C_B_TYPE = "1" *) 
(* C_B_VALUE = "10000001" *) (* C_B_WIDTH = "16" *) (* C_CCM_IMP = "0" *) 
(* C_CE_OVERRIDES_SCLR = "0" *) (* C_HAS_CE = "1" *) (* C_HAS_SCLR = "1" *) 
(* C_HAS_ZERO_DETECT = "0" *) (* C_LATENCY = "1" *) (* C_MODEL_TYPE = "0" *) 
(* C_MULT_TYPE = "1" *) (* C_OPTIMIZE_GOAL = "1" *) (* C_OUT_HIGH = "39" *) 
(* C_OUT_LOW = "0" *) (* C_ROUND_OUTPUT = "0" *) (* C_ROUND_PT = "0" *) 
(* C_VERBOSITY = "0" *) (* C_XDEVICEFAMILY = "artix7" *) (* ORIG_REF_NAME = "mult_gen_v12_0_14" *) 
(* downgradeipidentifiedwarnings = "yes" *) 
module resend_mult_mult_gen_v12_0_14
   (CLK,
    A,
    B,
    CE,
    SCLR,
    ZERO_DETECT,
    P,
    PCASC);
  input CLK;
  input [23:0]A;
  input [15:0]B;
  input CE;
  input SCLR;
  output [1:0]ZERO_DETECT;
  output [39:0]P;
  output [47:0]PCASC;

  wire \<const0> ;
  wire [23:0]A;
  wire [15:0]B;
  wire CE;
  wire CLK;
  wire [39:0]P;
  wire SCLR;
  wire [47:0]NLW_i_mult_PCASC_UNCONNECTED;
  wire [1:0]NLW_i_mult_ZERO_DETECT_UNCONNECTED;

  assign PCASC[47] = \<const0> ;
  assign PCASC[46] = \<const0> ;
  assign PCASC[45] = \<const0> ;
  assign PCASC[44] = \<const0> ;
  assign PCASC[43] = \<const0> ;
  assign PCASC[42] = \<const0> ;
  assign PCASC[41] = \<const0> ;
  assign PCASC[40] = \<const0> ;
  assign PCASC[39] = \<const0> ;
  assign PCASC[38] = \<const0> ;
  assign PCASC[37] = \<const0> ;
  assign PCASC[36] = \<const0> ;
  assign PCASC[35] = \<const0> ;
  assign PCASC[34] = \<const0> ;
  assign PCASC[33] = \<const0> ;
  assign PCASC[32] = \<const0> ;
  assign PCASC[31] = \<const0> ;
  assign PCASC[30] = \<const0> ;
  assign PCASC[29] = \<const0> ;
  assign PCASC[28] = \<const0> ;
  assign PCASC[27] = \<const0> ;
  assign PCASC[26] = \<const0> ;
  assign PCASC[25] = \<const0> ;
  assign PCASC[24] = \<const0> ;
  assign PCASC[23] = \<const0> ;
  assign PCASC[22] = \<const0> ;
  assign PCASC[21] = \<const0> ;
  assign PCASC[20] = \<const0> ;
  assign PCASC[19] = \<const0> ;
  assign PCASC[18] = \<const0> ;
  assign PCASC[17] = \<const0> ;
  assign PCASC[16] = \<const0> ;
  assign PCASC[15] = \<const0> ;
  assign PCASC[14] = \<const0> ;
  assign PCASC[13] = \<const0> ;
  assign PCASC[12] = \<const0> ;
  assign PCASC[11] = \<const0> ;
  assign PCASC[10] = \<const0> ;
  assign PCASC[9] = \<const0> ;
  assign PCASC[8] = \<const0> ;
  assign PCASC[7] = \<const0> ;
  assign PCASC[6] = \<const0> ;
  assign PCASC[5] = \<const0> ;
  assign PCASC[4] = \<const0> ;
  assign PCASC[3] = \<const0> ;
  assign PCASC[2] = \<const0> ;
  assign PCASC[1] = \<const0> ;
  assign PCASC[0] = \<const0> ;
  assign ZERO_DETECT[1] = \<const0> ;
  assign ZERO_DETECT[0] = \<const0> ;
  GND GND
       (.G(\<const0> ));
  (* C_A_TYPE = "1" *) 
  (* C_A_WIDTH = "24" *) 
  (* C_B_TYPE = "1" *) 
  (* C_B_VALUE = "10000001" *) 
  (* C_B_WIDTH = "16" *) 
  (* C_CCM_IMP = "0" *) 
  (* C_CE_OVERRIDES_SCLR = "0" *) 
  (* C_HAS_CE = "1" *) 
  (* C_HAS_SCLR = "1" *) 
  (* C_HAS_ZERO_DETECT = "0" *) 
  (* C_LATENCY = "1" *) 
  (* C_MODEL_TYPE = "0" *) 
  (* C_MULT_TYPE = "1" *) 
  (* C_OPTIMIZE_GOAL = "1" *) 
  (* C_OUT_HIGH = "39" *) 
  (* C_OUT_LOW = "0" *) 
  (* C_ROUND_OUTPUT = "0" *) 
  (* C_ROUND_PT = "0" *) 
  (* C_VERBOSITY = "0" *) 
  (* C_XDEVICEFAMILY = "artix7" *) 
  (* downgradeipidentifiedwarnings = "yes" *) 
  resend_mult_mult_gen_v12_0_14_viv i_mult
       (.A(A),
        .B(B),
        .CE(CE),
        .CLK(CLK),
        .P(P),
        .PCASC(NLW_i_mult_PCASC_UNCONNECTED[47:0]),
        .SCLR(SCLR),
        .ZERO_DETECT(NLW_i_mult_ZERO_DETECT_UNCONNECTED[1:0]));
endmodule
`pragma protect begin_protected
`pragma protect version = 1
`pragma protect encrypt_agent = "XILINX"
`pragma protect encrypt_agent_info = "Xilinx Encryption Tool 2015"
`pragma protect key_keyowner="Cadence Design Systems.", key_keyname="cds_rsa_key", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=64)
`pragma protect key_block
TvNAk+dzefmJC5/xfGEoXo1v1zzw15yvf2w3I+7pl9weHnOYLTwk2CtA6qQwUdiv+KPlR09XyHxt
UocEiAlS9g==

`pragma protect key_keyowner="Synopsys", key_keyname="SNPS-VCS-RSA-2", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=128)
`pragma protect key_block
ccd1Kr3IgmbU3Zd5R5UGhugxe9OUvTTk5M/+YDzRXyTvXIMaUxHB5fv7SuuebIYqGrGlL5seA2Sg
zO1i2uQFXVFn4M1DHS2E7BwirWBP5gmU/RaWKyEfTu3E5ZGbc1lvK67CCG8szRwdrvmY+Z8CpiC4
+fKoXg6GREReZgylTmE=

`pragma protect key_keyowner="Aldec", key_keyname="ALDEC15_001", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
D4OySXRBGdK3bWTwoBJnna9JJTCfjtow8OCB97TMc0CHJtgWscKG0sA6JP+WmQu+g/St8V3dnWCm
Z/oL2u8esW79WhsyQGAkuc2zUGutMTiH5JtlsxfFXreCjsbpfiQ4cOTSVV8RKFLaZCW+eXj7qQwk
WUd+Rk2Kp6kViZmb9GfGDSBc1qKbMuYuGLGiO+UVYNdt7dkYg9aAhJYx3c/Tx4m6BAZTpzEs9xzl
Mg0Plk7PRG/v5PXojT+9MvJ80iSqd3ejpG6kEE1mYBAhD1zmHQfbte6ipINFibjTuluuS5i0pIbf
HaA/nmULSj1xFBTfeEdDhm4CrFUWEdYvrJoOhg==

`pragma protect key_keyowner="ATRENTA", key_keyname="ATR-SG-2015-RSA-3", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
YmbWYAZhC3ayB3FdtHMbSkvV5OWWIi6gmohNfeiL3hZEqSlPd2B43zehv3FM2BA2v3N0HlGO0TL6
neUbRccVG37R0aVoXEjetzHP+ZMpVpr2wNRYoVv9EAzvD7YjPAyiMQMLJO1wmw/LJVkGpP4UCg4g
tgMS7M+LmVgeot1Fmcwa4mDyquYpShDC0ZhYtWL3VmO204ubc1HcI1fEQiMp+tBP7rYU0jIyGMtz
dXGUYS7PdIYkz5ApCjSfCCueqmWeZf9/KXMkoo9udSh2ZyT9uNr+GM8fH8rcz5nZjN4ShPghIUSN
XIZbR6KJ/+WqugC6B6ULpEZUxft3AS1vxij4dA==

`pragma protect key_keyowner="Xilinx", key_keyname="xilinxt_2017_05", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
pRgO0aX5waanQk0eZ4W7Q+LVxiXC+tf9hFRN9nsdM6xbA9apyUI0wd0pRjkzt/X5yvazLViQDSfS
Bm9cP+mYh23I891gOC2bMeto93RQUYlDhWmKA2HAuokJj6wKo/vk9LA0e/rAjHMWD7cTXHkdXPdz
d92x8sSRX6Z5gz0YOJ8hU+X3aLkMrr/d+Rs3UcELF+MTGSf53SzTuIbnaw08EsHUObyFusQxXlt6
ZuByaRiPP1ofEvMk+UCLRZThOA7sR6SIfjXOTF55TQgss4/Mf30sm+t84LW+xNBWIqVfiQ671PZF
CQ8K4qBj3nTT9D0FTUvfHdTmLtywWgV65+5W3A==

`pragma protect key_keyowner="Mentor Graphics Corporation", key_keyname="MGC-VELOCE-RSA", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=128)
`pragma protect key_block
d38DScsESf/yIfST5KEEwSUvjI+Km/dbua2xenGdzq3rgc/diAWKNIN11lcJIPDVBe6fB9J2TqbT
eXC+WnYP2YB9QXYlwKxLW7HOYcLC6Ivx9uoTg503B1azg5yB52W8iAwxelCieuRZ3qo4CxwOJ4w3
kwV+F675PsE0hWvEwTA=

`pragma protect key_keyowner="Mentor Graphics Corporation", key_keyname="MGC-VERIF-SIM-RSA-2", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
Bf4H+OH1vHHXYQ0B+xvr52Pkbk3t9R17gzpbDdSPXjerF+p1mOwTJrxL3jQRkm9rUtVIgJGiq2/s
crniU3gwf/UiAzOrNxcIp9eKlLwDNsxSMYn+mkUQWlDdifqNNVK+YFJD0ZFE6pzyWAfSd99uwvf2
B/+VXkZFAWz3devN4zOqXGE5+OZKTJNNH2fm+gcI0n7V4lPByrga5xMdlx99MQZZRprmMts+yOHQ
eVL2q0jneXaC7j4j8aSjRtpPAjf6aWk9xkdj2iVGAqs6TlpdNPyA9bKumNf3XCjAnjbNwxHWWAao
tHbBrxiXF1qQUoAzJ9mjy31tCjRX+JQOzKafLw==

`pragma protect key_keyowner="Mentor Graphics Corporation", key_keyname="MGC-PREC-RSA", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
b0YyM0LdrdvJyWZyUAz3uGlLPBHhxYyszx8vIsOqDz2XcHpicUmG1M7WnF4zIYBl2r9+0JMGpkn2
h81mO/Mmzyo3uFbXZibtHClUqln5rXrABhAp5qzGWtN1klUv143WfLklb/KSsQfY6tfZ/TworJ0D
T8P/XWbteFmqUaLdlsqWMM13FlKT6GOENT+qbBN+JrjoN6ufWOJHKG2fnOdh+D4JTz+GiNRTOFve
yvhm2liIUa7BQo96PBMSWE0lNRS2Xg3leZWmaDbA+wNbkFoaXlsk45rTmrnV2e539admSZaVMwU6
EAUu1c5gEiHUvlDBlUS/BgmHP6Yebs5opkO8Lg==

`pragma protect key_keyowner="Synplicity", key_keyname="SYNP15_1", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
0R5riioSYq3b1/PDp/QH7kPThpFA4Yxduimp7qO/ddj7sWr+0Cm1Q8xG7f9SmUDpZjamaSaBk+ts
vi3hC/MCuo9ENomfWLei92Jh2mtm+gKGx7wjLd29euiCU5mHCzE08QuIpYbF28PD+meQcU3pOmtY
8R800asg6+Snbhpo0+cFuxVvEdwmL1YzP+dk1u7v4+bxGGvFOX7+OTNKdgr2zeT9KDY1D8d2IEmT
lh1L+SW1G27nar/FwB/CsK3WtV0qUJ4NwHf9FudupWFlEei7UYE3WYzkLrAxMLhsP7ype5yDhzxx
ymZusFXbnJrOlIIgkv5FMwHdti4M7ZErjUE6nQ==

`pragma protect data_method = "AES128-CBC"
`pragma protect encoding = (enctype = "BASE64", line_length = 76, bytes = 7312)
`pragma protect data_block
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
Ucb0oHdpag/kZ30gyVRDPA==
`pragma protect end_protected
`ifndef GLBL
`define GLBL
`timescale  1 ps / 1 ps

module glbl ();

    parameter ROC_WIDTH = 100000;
    parameter TOC_WIDTH = 0;

//--------   STARTUP Globals --------------
    wire GSR;
    wire GTS;
    wire GWE;
    wire PRLD;
    tri1 p_up_tmp;
    tri (weak1, strong0) PLL_LOCKG = p_up_tmp;

    wire PROGB_GLBL;
    wire CCLKO_GLBL;
    wire FCSBO_GLBL;
    wire [3:0] DO_GLBL;
    wire [3:0] DI_GLBL;
   
    reg GSR_int;
    reg GTS_int;
    reg PRLD_int;

//--------   JTAG Globals --------------
    wire JTAG_TDO_GLBL;
    wire JTAG_TCK_GLBL;
    wire JTAG_TDI_GLBL;
    wire JTAG_TMS_GLBL;
    wire JTAG_TRST_GLBL;

    reg JTAG_CAPTURE_GLBL;
    reg JTAG_RESET_GLBL;
    reg JTAG_SHIFT_GLBL;
    reg JTAG_UPDATE_GLBL;
    reg JTAG_RUNTEST_GLBL;

    reg JTAG_SEL1_GLBL = 0;
    reg JTAG_SEL2_GLBL = 0 ;
    reg JTAG_SEL3_GLBL = 0;
    reg JTAG_SEL4_GLBL = 0;

    reg JTAG_USER_TDO1_GLBL = 1'bz;
    reg JTAG_USER_TDO2_GLBL = 1'bz;
    reg JTAG_USER_TDO3_GLBL = 1'bz;
    reg JTAG_USER_TDO4_GLBL = 1'bz;

    assign (strong1, weak0) GSR = GSR_int;
    assign (strong1, weak0) GTS = GTS_int;
    assign (weak1, weak0) PRLD = PRLD_int;

    initial begin
	GSR_int = 1'b1;
	PRLD_int = 1'b1;
	#(ROC_WIDTH)
	GSR_int = 1'b0;
	PRLD_int = 1'b0;
    end

    initial begin
	GTS_int = 1'b1;
	#(TOC_WIDTH)
	GTS_int = 1'b0;
    end

endmodule
`endif
