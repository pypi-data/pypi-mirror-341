// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top__Syms.h"
#include "Vff_top___024unit__03a__03atransaction__Vclpkg.h"

Vff_top___024unit__03a__03atransaction::Vff_top___024unit__03a__03atransaction(Vff_top__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::new\n"); );
    // Init
    _ctor_var_reset(vlSymsp);
}

void Vff_top___024unit__03a__03atransaction::_ctor_var_reset(Vff_top__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::_ctor_var_reset\n"); );
    // Body
    (void)vlSymsp;  // Prevent unused variable warning
    __PVT__data_in = 0;
    __PVT__reset_in = 0;
    __PVT__data_out = 0;
}
