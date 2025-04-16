// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top__Syms.h"
#include "Vff_top___024unit__03a__03atesting_env__Vclpkg.h"

Vff_top___024unit__03a__03atesting_env::Vff_top___024unit__03a__03atesting_env(Vff_top__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::new\n"); );
    // Init
    _ctor_var_reset(vlSymsp);
    // Body
    this->__PVT__rn = 0U;
    this->__PVT__a = 0U;
    this->__PVT__reset_prob = 0U;
    this->__PVT__iter = 0U;
}

void Vff_top___024unit____Vdpiimwrap_test_TOP____024unit(IData/*31:0*/ a, IData/*31:0*/ &test__Vfuncrtn);

void Vff_top___024unit__03a__03atesting_env::__VnoInFunc_read_config(Vff_top__Syms* __restrict vlSymsp, std::string filename) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::__VnoInFunc_read_config\n"); );
    // Init
    IData/*31:0*/ __Vfunc_test__0__Vfuncout;
    __Vfunc_test__0__Vfuncout = 0;
    // Body
    IData/*31:0*/ file;
    file = 0;
    IData/*31:0*/ value;
    value = 0;
    std::string param;
    VL_WRITEF_NX("Test: %x\n",0,32,([&]() {
                    Vff_top___024unit____Vdpiimwrap_test_TOP____024unit(0U, __Vfunc_test__0__Vfuncout);
                }(), __Vfunc_test__0__Vfuncout));
    file = VL_FOPEN_NN(VL_CVT_PACK_STR_NN(filename)
                       , std::string{"r"});
    ;
    while ((! (file ? feof(VL_CVT_I_FP(file)) : true))) {
        (void)VL_FSCANF_INX(file,"%s %#",0,-1,&(param),
                            32,&(value)) ;
        if ((std::string{"ITERATIONS"} == param)) {
            this->__PVT__iter = value;
        } else if ((std::string{"RESET_PROB"} == param)) {
            this->__PVT__reset_prob = value;
        }
    }
}

void Vff_top___024unit__03a__03atesting_env::_ctor_var_reset(Vff_top__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::_ctor_var_reset\n"); );
    // Body
    (void)vlSymsp;  // Prevent unused variable warning
    __PVT__rn = 0;
    __PVT__a = 0;
    __PVT__reset_prob = 0;
    __PVT__iter = 0;
}
