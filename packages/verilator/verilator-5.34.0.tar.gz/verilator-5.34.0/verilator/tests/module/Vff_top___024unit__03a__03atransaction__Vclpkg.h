// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vff_top.h for the primary calling header

#ifndef VERILATED_VFF_TOP___024UNIT__03A__03ATRANSACTION__VCLPKG_H_
#define VERILATED_VFF_TOP___024UNIT__03A__03ATRANSACTION__VCLPKG_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"
#include "verilated_random.h"


class Vff_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vff_top___024unit__03a__03atransaction__Vclpkg final : public VerilatedModule {
  public:

    // INTERNAL VARIABLES
    Vff_top__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vff_top___024unit__03a__03atransaction__Vclpkg(Vff_top__Syms* symsp, const char* v__name);
    ~Vff_top___024unit__03a__03atransaction__Vclpkg();
    VL_UNCOPYABLE(Vff_top___024unit__03a__03atransaction__Vclpkg);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


class Vff_top__Syms;

class Vff_top___024unit__03a__03atransaction : public VlClass {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ __PVT__reset_in;
    IData/*31:0*/ __PVT__data_in;
    IData/*31:0*/ __PVT__data_out;
    void __VnoInFunc_check_output(Vff_top__Syms* __restrict vlSymsp, IData/*31:0*/ dut_out, CData/*0:0*/ &check_output__Vfuncrtn);
    void __VnoInFunc_clock(Vff_top__Syms* __restrict vlSymsp);
    void __VnoInFunc_set_inputs(Vff_top__Syms* __restrict vlSymsp, CData/*0:0*/ dut_reset, IData/*31:0*/ dut_in);
  private:
    void _ctor_var_reset(Vff_top__Syms* __restrict vlSymsp);
  public:
    Vff_top___024unit__03a__03atransaction(Vff_top__Syms* __restrict vlSymsp);
    std::string to_string() const;
    std::string to_string_middle() const;
    ~Vff_top___024unit__03a__03atransaction();
};

std::string VL_TO_STRING(const VlClassRef<Vff_top___024unit__03a__03atransaction>& obj);

#endif  // guard
