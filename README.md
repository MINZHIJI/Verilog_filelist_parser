# Verilog FileList Parser

THe project is for parsing filelist in Verilog.
Usually we will write Verilog file list to integrate our IP or Subsystem.
However, we may need to check the files in the file lists, we will face something painful.
So I want to write a parser to parse the file list for Verilog Simulator.

## Support

I will support format in Synopsys Simulator(VCS) and Cadence Simulator(Xcelium).
We will use `-f` to import the file list of Verilog.
However, the file list is just a small command set in those simulators.
So we can write more specicial commands with the corresponding simulator.
For example, `+incdir+<including_dir>`
So we need to support some features about those commands.
