// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vff_top.h for the primary calling header

#ifndef VERILATED_VFF_TOP_FF_IFC_H_
#define VERILATED_VFF_TOP_FF_IFC_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"
#include "verilated_random.h"


class Vff_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vff_top_ff_ifc final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    CData/*0:0*/ reset;
    CData/*0:0*/ valid_i;
    IData/*31:0*/ data_i;

    // INTERNAL VARIABLES
    Vff_top__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vff_top_ff_ifc(Vff_top__Syms* symsp, const char* v__name);
    ~Vff_top_ff_ifc();
    VL_UNCOPYABLE(Vff_top_ff_ifc);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};

std::string VL_TO_STRING(const Vff_top_ff_ifc* obj);

#endif  // guard
