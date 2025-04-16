// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top__Syms.h"
#include "Vff_top___024unit.h"

void Vff_top___024unit___ctor_var_reset(Vff_top___024unit* vlSelf);

Vff_top___024unit::Vff_top___024unit(Vff_top__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , vlSymsp{symsp}
 {
    // Reset structure values
    Vff_top___024unit___ctor_var_reset(this);
}

void Vff_top___024unit::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vff_top___024unit::~Vff_top___024unit() {
}
