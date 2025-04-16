// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals
#include "verilated_vcd_c.h"
#include "Vff_top__Syms.h"


void Vff_top___024root__trace_chg_0_sub_0(Vff_top___024root* vlSelf, VerilatedVcd::Buffer* bufp);

void Vff_top___024root__trace_chg_0(void* voidSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root__trace_chg_0\n"); );
    // Init
    Vff_top___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vff_top___024root*>(voidSelf);
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    if (VL_UNLIKELY(!vlSymsp->__Vm_activity)) return;
    // Body
    Vff_top___024root__trace_chg_0_sub_0((&vlSymsp->TOP), bufp);
}

void Vff_top___024root__trace_chg_0_sub_0(Vff_top___024root* vlSelf, VerilatedVcd::Buffer* bufp) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root__trace_chg_0_sub_0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    uint32_t* const oldp VL_ATTR_UNUSED = bufp->oldp(vlSymsp->__Vm_baseCode + 1);
    // Body
    if (VL_UNLIKELY((vlSelfRef.__Vm_traceActivity[1U] 
                     | vlSelfRef.__Vm_traceActivity
                     [2U]))) {
        bufp->chgBit(oldp+0,(vlSelfRef.ff_top__DOT__bench__DOT__result));
        bufp->chgBit(oldp+1,(vlSelfRef.ff_top__DOT__bench__DOT__pass));
        bufp->chgBit(oldp+2,(vlSymsp->TOP__ff_top__DOT__IFC.reset));
        bufp->chgBit(oldp+3,(vlSymsp->TOP__ff_top__DOT__IFC.valid_i));
        bufp->chgIData(oldp+4,(vlSymsp->TOP__ff_top__DOT__IFC.data_i),32);
    }
    bufp->chgBit(oldp+5,(vlSelfRef.clk));
    bufp->chgIData(oldp+6,(vlSelfRef.ff_top__DOT__dut__DOT__data),32);
    bufp->chgBit(oldp+7,(vlSelfRef.ff_top__DOT__dut__DOT__valid));
}

void Vff_top___024root__trace_cleanup(void* voidSelf, VerilatedVcd* /*unused*/) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root__trace_cleanup\n"); );
    // Init
    Vff_top___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vff_top___024root*>(voidSelf);
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    // Body
    vlSymsp->__Vm_activity = false;
    vlSymsp->TOP.__Vm_traceActivity[0U] = 0U;
    vlSymsp->TOP.__Vm_traceActivity[1U] = 0U;
    vlSymsp->TOP.__Vm_traceActivity[2U] = 0U;
}
