# Verilated -*- Makefile -*-
# DESCRIPTION: Verilator output: Make include file with class lists
#
# This file lists generated Verilated files, for including in higher level makefiles.
# See Vff_top.mk for the caller.

### Switches...
# C11 constructs required?  0/1 (always on now)
VM_C11 = 1
# Timing enabled?  0/1
VM_TIMING = 1
# Coverage output mode?  0/1 (from --coverage)
VM_COVERAGE = 0
# Parallel builds?  0/1 (from --output-split)
VM_PARALLEL_BUILDS = 0
# Tracing output mode?  0/1 (from --trace/--trace-fst)
VM_TRACE = 1
# Tracing output mode in VCD format?  0/1 (from --trace)
VM_TRACE_VCD = 1
# Tracing output mode in FST format?  0/1 (from --trace-fst)
VM_TRACE_FST = 0

### Object file lists...
# Generated module classes, fast-path, compile with highest optimization
VM_CLASSES_FAST += \
	Vff_top \
	Vff_top___024root__DepSet_hefd428be__0 \
	Vff_top___024root__DepSet_h9de4ad84__0 \
	Vff_top___024root__DepSet_hc96c556c__0 \
	Vff_top___024unit__DepSet_h409fbc44__0 \
	Vff_top_ff_ifc__DepSet_hf19b9e84__0 \
	Vff_top___024unit__03a__03atransaction__Vclpkg__DepSet_h1d6fc69b__0 \
	Vff_top___024unit__03a__03atransaction__Vclpkg__DepSet_h17c2e74f__0 \
	Vff_top___024unit__03a__03atesting_env__Vclpkg__DepSet_h321f5b92__0 \
	Vff_top___024unit__03a__03atesting_env__Vclpkg__DepSet_heeb38458__0 \

# Generated module classes, non-fast-path, compile with low/medium optimization
VM_CLASSES_SLOW += \
	Vff_top___024root__Slow \
	Vff_top___024root__DepSet_hefd428be__0__Slow \
	Vff_top___024root__DepSet_hc96c556c__0__Slow \
	Vff_top___024unit__Slow \
	Vff_top___024unit__DepSet_h5c32e1a2__0__Slow \
	Vff_top_ff_ifc__Slow \
	Vff_top_ff_ifc__DepSet_hf19b9e84__0__Slow \
	Vff_top___024unit__03a__03atransaction__Vclpkg__Slow \
	Vff_top___024unit__03a__03atransaction__Vclpkg__DepSet_h17c2e74f__0__Slow \
	Vff_top___024unit__03a__03atesting_env__Vclpkg__Slow \
	Vff_top___024unit__03a__03atesting_env__Vclpkg__DepSet_heeb38458__0__Slow \

# Generated support classes, fast-path, compile with highest optimization
VM_SUPPORT_FAST += \
	Vff_top__Dpi \
	Vff_top__Trace__0 \

# Generated support classes, non-fast-path, compile with low/medium optimization
VM_SUPPORT_SLOW += \
	Vff_top__Syms \
	Vff_top__Trace__0__Slow \
	Vff_top__TraceDecls__0__Slow \

# Global classes, need linked once per executable, fast-path, compile with highest optimization
VM_GLOBAL_FAST += \
	verilated \
	verilated_dpi \
	verilated_vcd_c \
	verilated_timing \
	verilated_random \
	verilated_threads \

# Global classes, need linked once per executable, non-fast-path, compile with low/medium optimization
VM_GLOBAL_SLOW += \


# Verilated -*- Makefile -*-
