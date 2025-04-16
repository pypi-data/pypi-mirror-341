// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top__Syms.h"
#include "Vff_top___024unit.h"

extern "C" int test(int a);

VL_INLINE_OPT void Vff_top___024unit____Vdpiimwrap_test_TOP____024unit(IData/*31:0*/ a, IData/*31:0*/ &test__Vfuncrtn) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vff_top___024unit____Vdpiimwrap_test_TOP____024unit\n"); );
    // Body
    int a__Vcvt;
    for (size_t a__Vidx = 0; a__Vidx < 1; ++a__Vidx) a__Vcvt = a;
    int test__Vfuncrtn__Vcvt;
    test__Vfuncrtn__Vcvt = test(a__Vcvt);
    test__Vfuncrtn = test__Vfuncrtn__Vcvt;
}
