// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top___024unit__03a__03atransaction__Vclpkg.h"

void Vff_top___024unit__03a__03atransaction::__VnoInFunc_set_inputs(Vff_top__Syms* __restrict vlSymsp, CData/*0:0*/ dut_reset, IData/*31:0*/ dut_in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::__VnoInFunc_set_inputs\n"); );
    // Body
    this->__PVT__data_in = dut_in;
    this->__PVT__reset_in = dut_reset;
}

void Vff_top___024unit__03a__03atransaction::__VnoInFunc_clock(Vff_top__Syms* __restrict vlSymsp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::__VnoInFunc_clock\n"); );
    // Body
    this->__PVT__data_out = ((IData)(this->__PVT__reset_in)
                              ? 0U : this->__PVT__data_in);
}

void Vff_top___024unit__03a__03atransaction::__VnoInFunc_check_output(Vff_top__Syms* __restrict vlSymsp, IData/*31:0*/ dut_out, CData/*0:0*/ &check_output__Vfuncrtn) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::__VnoInFunc_check_output\n"); );
    // Body
    check_output__Vfuncrtn = (dut_out == this->__PVT__data_out);
}

Vff_top___024unit__03a__03atransaction::~Vff_top___024unit__03a__03atransaction() {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::~\n"); );
}

std::string VL_TO_STRING(const VlClassRef<Vff_top___024unit__03a__03atransaction>& obj) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::VL_TO_STRING\n"); );
    // Body
    return (obj ? obj->to_string() : "null");
}

std::string Vff_top___024unit__03a__03atransaction::to_string() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::to_string\n"); );
    // Body
    return ("'{"s + to_string_middle() + "}");
}

std::string Vff_top___024unit__03a__03atransaction::to_string_middle() const {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top___024unit__03a__03atransaction::to_string_middle\n"); );
    // Body
    std::string out;
    out += "data_in:" + VL_TO_STRING(__PVT__data_in);
    out += ", reset_in:" + VL_TO_STRING(__PVT__reset_in);
    out += ", data_out:" + VL_TO_STRING(__PVT__data_out);
    return out;
}
