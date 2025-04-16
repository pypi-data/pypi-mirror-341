// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top__Syms.h"
#include "Vff_top___024root.h"
#include "Vff_top___024unit__03a__03atesting_env__Vclpkg.h"
#include "Vff_top___024unit__03a__03atransaction__Vclpkg.h"

VL_INLINE_OPT VlCoroutine Vff_top___024root___eval_initial__TOP__Vtiming__0(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_initial__TOP__Vtiming__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlClassRef<Vff_top___024unit__03a__03atransaction> ff_top__DOT__bench__DOT__t;
    VlClassRef<Vff_top___024unit__03a__03atesting_env> ff_top__DOT__bench__DOT__v;
    IData/*31:0*/ ff_top__DOT__bench__DOT__unnamedblk1_2__DOT____Vrepeat1;
    ff_top__DOT__bench__DOT__unnamedblk1_2__DOT____Vrepeat1 = 0;
    IData/*31:0*/ __Vtask_randomize__3__Vfuncout;
    __Vtask_randomize__3__Vfuncout = 0;
    CData/*0:0*/ __Vtask_check_output__6__Vfuncout;
    __Vtask_check_output__6__Vfuncout = 0;
    // Body
    ff_top__DOT__bench__DOT__t = VL_NEW(Vff_top___024unit__03a__03atransaction, vlSymsp);
    ff_top__DOT__bench__DOT__v = VL_NEW(Vff_top___024unit__03a__03atesting_env, vlSymsp);
    VL_NULL_CHECK(ff_top__DOT__bench__DOT__v, "verilator/tests/module/ff_tb.sv", 14)->__VnoInFunc_read_config(vlSymsp, 
                                                                                std::string{"config.txt"});
    vlSelfRef.ff_top__DOT__bench__DOT__pass = 1U;
    vlSymsp->TOP__ff_top__DOT__IFC.reset = 1U;
    co_await vlSelfRef.__VtrigSched_h08f81b40__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge clk)", 
                                                         "verilator/tests/module/ff_tb.sv", 
                                                         20);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    vlSymsp->TOP__ff_top__DOT__IFC.reset = 1U;
    co_await vlSelfRef.__VtrigSched_h08f81b40__0.trigger(0U, 
                                                         nullptr, 
                                                         "@(posedge clk)", 
                                                         "verilator/tests/module/ff_tb.sv", 
                                                         20);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    ff_top__DOT__bench__DOT__unnamedblk1_2__DOT____Vrepeat1 
        = VL_NULL_CHECK(ff_top__DOT__bench__DOT__v, "verilator/tests/module/ff_tb.sv", 25)
        ->__PVT__iter;
    while (VL_LTS_III(32, 0U, ff_top__DOT__bench__DOT__unnamedblk1_2__DOT____Vrepeat1)) {
        VL_NULL_CHECK(ff_top__DOT__bench__DOT__v, "verilator/tests/module/ff_tb.sv", 26)->__VnoInFunc_randomize(vlSymsp, __Vtask_randomize__3__Vfuncout);
        vlSymsp->TOP__ff_top__DOT__IFC.reset = 0U;
        vlSymsp->TOP__ff_top__DOT__IFC.valid_i = 1U;
        vlSymsp->TOP__ff_top__DOT__IFC.data_i = VL_MODDIV_III(32, (IData)(VL_NULL_CHECK(ff_top__DOT__bench__DOT__v, "verilator/tests/module/ff_tb.sv", 30)
                                                                          ->__PVT__a), (IData)(0x64U));
        VL_NULL_CHECK(ff_top__DOT__bench__DOT__t, "verilator/tests/module/ff_tb.sv", 31)->__VnoInFunc_set_inputs(vlSymsp, 0U, 
                                                                                VL_MODDIV_III(32, (IData)(VL_NULL_CHECK(ff_top__DOT__bench__DOT__v, "verilator/tests/module/ff_tb.sv", 31)
                                                                                ->__PVT__a), (IData)(0x64U)));
        co_await vlSelfRef.__VtrigSched_h08f81b40__0.trigger(0U, 
                                                             nullptr, 
                                                             "@(posedge clk)", 
                                                             "verilator/tests/module/ff_tb.sv", 
                                                             33);
        vlSelfRef.__Vm_traceActivity[2U] = 1U;
        VL_NULL_CHECK(ff_top__DOT__bench__DOT__t, "verilator/tests/module/ff_tb.sv", 35)->__VnoInFunc_clock(vlSymsp);
        VL_NULL_CHECK(ff_top__DOT__bench__DOT__t, "verilator/tests/module/ff_tb.sv", 36)->__VnoInFunc_check_output(vlSymsp, vlSelfRef.ff_top__DOT__dut__DOT__data, __Vtask_check_output__6__Vfuncout);
        vlSelfRef.ff_top__DOT__bench__DOT__result = __Vtask_check_output__6__Vfuncout;
        VL_WRITEF_NX("[%0^]\texpected[%0#] == actual[%0#]\t%s\n",0,
                     64,VL_TIME_UNITED_D(1),-9,32,VL_NULL_CHECK(ff_top__DOT__bench__DOT__t, "verilator/tests/module/ff_tb.sv", 37)
                     ->__PVT__data_out,32,vlSelfRef.ff_top__DOT__dut__DOT__data,
                     32,((IData)(vlSelfRef.ff_top__DOT__bench__DOT__result)
                          ? 0x50415353U : 0x4641494cU));
        vlSelfRef.ff_top__DOT__bench__DOT__pass = ((IData)(vlSelfRef.ff_top__DOT__bench__DOT__pass) 
                                                   & (IData)(vlSelfRef.ff_top__DOT__bench__DOT__result));
        ff_top__DOT__bench__DOT__unnamedblk1_2__DOT____Vrepeat1 
            = (ff_top__DOT__bench__DOT__unnamedblk1_2__DOT____Vrepeat1 
               - (IData)(1U));
    }
    if (vlSymsp->_vm_contextp__->assertOnGet(2, 1)) {
        if (VL_UNLIKELY((1U & (~ (IData)(vlSelfRef.ff_top__DOT__bench__DOT__pass))))) {
            VL_WRITEF_NX("[%0t] %%Fatal: ff_tb.sv:42: Assertion failed in %Nff_top.bench: Test failed\n",0,
                         64,VL_TIME_UNITED_Q(1),-9,
                         vlSymsp->name());
            VL_STOP_MT("verilator/tests/module/ff_tb.sv", 42, "", false);
        }
    }
    VL_FINISH_MT("verilator/tests/module/ff_tb.sv", 43, "");
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
}
