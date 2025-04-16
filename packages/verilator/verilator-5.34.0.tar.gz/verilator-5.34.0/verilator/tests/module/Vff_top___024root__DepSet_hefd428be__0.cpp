// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top__Syms.h"
#include "Vff_top___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vff_top___024root___dump_triggers__act(Vff_top___024root* vlSelf);
#endif  // VL_DEBUG

void Vff_top___024root___eval_triggers__act(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_triggers__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered.set(0U, ((IData)(vlSelfRef.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))));
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vff_top___024root___dump_triggers__act(vlSelf);
    }
#endif
}

VL_INLINE_OPT void Vff_top___024root___nba_sequent__TOP__0(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___nba_sequent__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.ff_top__DOT__dut__DOT__valid = ((1U & 
                                               (~ (IData)(vlSymsp->TOP__ff_top__DOT__IFC.reset))) 
                                              && (IData)(vlSymsp->TOP__ff_top__DOT__IFC.valid_i));
    if (vlSymsp->TOP__ff_top__DOT__IFC.reset) {
        vlSelfRef.ff_top__DOT__dut__DOT__data = 0U;
    } else if (vlSymsp->TOP__ff_top__DOT__IFC.valid_i) {
        vlSelfRef.ff_top__DOT__dut__DOT__data = vlSymsp->TOP__ff_top__DOT__IFC.data_i;
    }
}
