// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top___024unit__03a__03atesting_env__Vclpkg.h"

void Vff_top___024unit__03a__03atesting_env::__VnoInFunc_get_reset(Vff_top__Syms* __restrict vlSymsp, CData/*0:0*/ &get_reset__Vfuncrtn) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::__VnoInFunc_get_reset\n"); );
    // Body
    get_reset__Vfuncrtn = (VL_MODDIV_III(32, this->__PVT__rn, (IData)(0x64U)) 
                           < this->__PVT__reset_prob);
}

void Vff_top___024unit__03a__03atesting_env::__VnoInFunc_randomize(Vff_top__Syms* __restrict vlSymsp, IData/*31:0*/ &randomize__Vfuncrtn) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::__VnoInFunc_randomize\n"); );
    // Init
    IData/*31:0*/ __Vfunc___Vbasic_randomize__1__Vfuncout;
    __Vfunc___Vbasic_randomize__1__Vfuncout = 0;
    // Body
    randomize__Vfuncrtn = 1U;
    randomize__Vfuncrtn = (1U & ([&]() {
                this->__VnoInFunc___Vbasic_randomize(vlSymsp, __Vfunc___Vbasic_randomize__1__Vfuncout);
            }(), __Vfunc___Vbasic_randomize__1__Vfuncout));
}

void Vff_top___024unit__03a__03atesting_env::__VnoInFunc___Vbasic_randomize(Vff_top__Syms* __restrict vlSymsp, IData/*31:0*/ &__Vbasic_randomize__Vfuncrtn) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::__VnoInFunc___Vbasic_randomize\n"); );
    // Body
    __Vbasic_randomize__Vfuncrtn = 1U;
    this->__PVT__rn = VL_RANDOM_RNG_I(__Vm_rng);
    this->__PVT__a = VL_RANDOM_RNG_I(__Vm_rng);
}

Vff_top___024unit__03a__03atesting_env::~Vff_top___024unit__03a__03atesting_env() {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::~\n"); );
}

std::string VL_TO_STRING(const VlClassRef<Vff_top___024unit__03a__03atesting_env>& obj) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::VL_TO_STRING\n"); );
    // Body
    return (obj ? obj->to_string() : "null");
}

std::string Vff_top___024unit__03a__03atesting_env::to_string() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::to_string\n"); );
    // Body
    return ("'{"s + to_string_middle() + "}");
}

std::string Vff_top___024unit__03a__03atesting_env::to_string_middle() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atesting_env::to_string_middle\n"); );
    // Body
    std::string out;
    out += "rn:" + VL_TO_STRING(__PVT__rn);
    out += ", a:" + VL_TO_STRING(__PVT__a);
    out += ", reset_prob:" + VL_TO_STRING(__PVT__reset_prob);
    out += ", iter:" + VL_TO_STRING(__PVT__iter);
    return out;
}
