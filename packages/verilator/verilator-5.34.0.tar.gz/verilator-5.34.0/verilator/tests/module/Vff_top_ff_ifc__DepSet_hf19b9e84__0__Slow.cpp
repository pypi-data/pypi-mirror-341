// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top_ff_ifc.h"

VL_ATTR_COLD void Vff_top_ff_ifc___ctor_var_reset(Vff_top_ff_ifc* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top_ff_ifc___ctor_var_reset\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->clk = 0;
    vlSelf->reset = VL_RAND_RESET_I(1);
    vlSelf->valid_i = VL_RAND_RESET_I(1);
    vlSelf->data_i = VL_RAND_RESET_I(32);
}
