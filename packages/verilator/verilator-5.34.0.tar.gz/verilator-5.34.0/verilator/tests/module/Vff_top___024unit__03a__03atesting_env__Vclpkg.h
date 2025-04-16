// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vff_top.h for the primary calling header

#ifndef VERILATED_VFF_TOP___024UNIT__03A__03ATESTING_ENV__VCLPKG_H_
#define VERILATED_VFF_TOP___024UNIT__03A__03ATESTING_ENV__VCLPKG_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"
#include "verilated_random.h"


class Vff_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vff_top___024unit__03a__03atesting_env__Vclpkg final : public VerilatedModule {
  public:

    // INTERNAL VARIABLES
    Vff_top__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vff_top___024unit__03a__03atesting_env__Vclpkg(Vff_top__Syms* symsp, const char* v__name);
    ~Vff_top___024unit__03a__03atesting_env__Vclpkg();
    VL_UNCOPYABLE(Vff_top___024unit__03a__03atesting_env__Vclpkg);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


class Vff_top__Syms;

class Vff_top___024unit__03a__03atesting_env : public VlClass {
  public:

    // DESIGN SPECIFIC STATE
    IData/*31:0*/ __PVT__rn;
    IData/*31:0*/ __PVT__a;
    IData/*31:0*/ __PVT__reset_prob;
    IData/*31:0*/ __PVT__iter;

    // INTERNAL VARIABLES
    VlRNG __Vm_rng;
    void __VnoInFunc___Vbasic_randomize(Vff_top__Syms* __restrict vlSymsp, IData/*31:0*/ &__Vbasic_randomize__Vfuncrtn);
    void __VnoInFunc_get_reset(Vff_top__Syms* __restrict vlSymsp, CData/*0:0*/ &get_reset__Vfuncrtn);
    void __VnoInFunc_randomize(Vff_top__Syms* __restrict vlSymsp, IData/*31:0*/ &randomize__Vfuncrtn);
    void __VnoInFunc_read_config(Vff_top__Syms* __restrict vlSymsp, std::string filename);
  private:
    void _ctor_var_reset(Vff_top__Syms* __restrict vlSymsp);
  public:
    Vff_top___024unit__03a__03atesting_env(Vff_top__Syms* __restrict vlSymsp);
    std::string to_string() const;
    std::string to_string_middle() const;
    ~Vff_top___024unit__03a__03atesting_env();
};

std::string VL_TO_STRING(const VlClassRef<Vff_top___024unit__03a__03atesting_env>& obj);

#endif  // guard
