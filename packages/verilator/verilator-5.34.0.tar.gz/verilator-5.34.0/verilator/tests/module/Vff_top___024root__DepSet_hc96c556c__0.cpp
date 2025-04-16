// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top___024root.h"

VL_ATTR_COLD void Vff_top___024root___eval_initial__TOP(Vff_top___024root* vlSelf);
VlCoroutine Vff_top___024root___eval_initial__TOP__Vtiming__0(Vff_top___024root* vlSelf);

void Vff_top___024root___eval_initial(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_initial\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vff_top___024root___eval_initial__TOP(vlSelf);
    vlSelfRef.__Vm_traceActivity[1U] = 1U;
    Vff_top___024root___eval_initial__TOP__Vtiming__0(vlSelf);
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
}

void Vff_top___024root___eval_act(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

void Vff_top___024root___nba_sequent__TOP__0(Vff_top___024root* vlSelf);

void Vff_top___024root___eval_nba(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vff_top___024root___nba_sequent__TOP__0(vlSelf);
    }
}

void Vff_top___024root___timing_commit(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___timing_commit\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((! (1ULL & vlSelfRef.__VactTriggered.word(0U)))) {
        vlSelfRef.__VtrigSched_h08f81b40__0.commit(
                                                   "@(posedge clk)");
    }
}

void Vff_top___024root___timing_resume(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___timing_resume\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        vlSelfRef.__VtrigSched_h08f81b40__0.resume(
                                                   "@(posedge clk)");
    }
}

void Vff_top___024root___eval_triggers__act(Vff_top___024root* vlSelf);

bool Vff_top___024root___eval_phase__act(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_phase__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<1> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vff_top___024root___eval_triggers__act(vlSelf);
    Vff_top___024root___timing_commit(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        Vff_top___024root___timing_resume(vlSelf);
        Vff_top___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vff_top___024root___eval_phase__nba(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_phase__nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vff_top___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vff_top___024root___dump_triggers__nba(Vff_top___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vff_top___024root___dump_triggers__act(Vff_top___024root* vlSelf);
#endif  // VL_DEBUG

void Vff_top___024root___eval(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            Vff_top___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("verilator/tests/module/ff_top.sv", 3, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelfRef.__VactIterCount))) {
#ifdef VL_DEBUG
                Vff_top___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("verilator/tests/module/ff_top.sv", 3, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (Vff_top___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (Vff_top___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vff_top___024root___eval_debug_assertions(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_debug_assertions\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY((vlSelfRef.clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
}
#endif  // VL_DEBUG
