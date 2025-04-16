// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vff_top.h for the primary calling header

#ifndef VERILATED_VFF_TOP___024UNIT_H_
#define VERILATED_VFF_TOP___024UNIT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"
#include "verilated_random.h"


class Vff_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vff_top___024unit final : public VerilatedModule {
  public:

    // INTERNAL VARIABLES
    Vff_top__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vff_top___024unit(Vff_top__Syms* symsp, const char* v__name);
    ~Vff_top___024unit();
    VL_UNCOPYABLE(Vff_top___024unit);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
