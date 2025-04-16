// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vff_top.h for the primary calling header

#ifndef VERILATED_VFF_TOP___024ROOT_H_
#define VERILATED_VFF_TOP___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"
#include "verilated_random.h"
class Vff_top___024unit;
class Vff_top___024unit__03a__03atesting_env;
class Vff_top___024unit__03a__03atesting_env__Vclpkg;
class Vff_top___024unit__03a__03atransaction;
class Vff_top___024unit__03a__03atransaction__Vclpkg;
class Vff_top_ff_ifc;


class Vff_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vff_top___024root final : public VerilatedModule {
  public:
    // CELLS
    Vff_top___024unit* __PVT____024unit;
    Vff_top_ff_ifc* __PVT__ff_top__DOT__IFC;
    Vff_top___024unit__03a__03atransaction__Vclpkg* __024unit__03a__03atransaction__Vclpkg;
    Vff_top___024unit__03a__03atesting_env__Vclpkg* __024unit__03a__03atesting_env__Vclpkg;

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    CData/*0:0*/ ff_top__DOT__dut__DOT__valid;
    CData/*0:0*/ ff_top__DOT__bench__DOT__result;
    CData/*0:0*/ ff_top__DOT__bench__DOT__pass;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __VactContinue;
    IData/*31:0*/ ff_top__DOT__dut__DOT__data;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<CData/*0:0*/, 3> __Vm_traceActivity;
    VlTriggerScheduler __VtrigSched_h08f81b40__0;
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vff_top__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vff_top___024root(Vff_top__Syms* symsp, const char* v__name);
    ~Vff_top___024root();
    VL_UNCOPYABLE(Vff_top___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
