// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top__Syms.h"
#include "Vff_top___024root.h"

VL_ATTR_COLD void Vff_top___024root___eval_initial__TOP(Vff_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vff_top___024root___eval_initial__TOP\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlWide<4>/*127:0*/ __Vtemp_1;
    // Body
    VL_WRITEF_NX("[%0t]\tTracing to logs/dump.vcd...\n",0,
                 64,VL_TIME_UNITED_Q(1),-9);
    __Vtemp_1[0U] = 0x2e766364U;
    __Vtemp_1[1U] = 0x64756d70U;
    __Vtemp_1[2U] = 0x6f67732fU;
    __Vtemp_1[3U] = 0x6cU;
    vlSymsp->_vm_contextp__->dumpfile(VL_CVT_PACK_STR_NW(4, __Vtemp_1));
    vlSymsp->_traceDumpOpen();
    VL_WRITEF_NX("[%0t]\tModel running...\n",0,64,VL_TIME_UNITED_Q(1),
                 -9);
}
