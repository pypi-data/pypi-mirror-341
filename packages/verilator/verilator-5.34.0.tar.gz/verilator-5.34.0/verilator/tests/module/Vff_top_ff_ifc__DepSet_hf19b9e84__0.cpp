// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vff_top.h for the primary calling header

#include "Vff_top__pch.h"
#include "Vff_top_ff_ifc.h"

std::string VL_TO_STRING(const Vff_top_ff_ifc* obj) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vff_top_ff_ifc::VL_TO_STRING\n"); );
    // Body
    return (obj ? obj->name() : "null");
}
