// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VFF_TOP__SYMS_H_
#define VERILATED_VFF_TOP__SYMS_H_  // guard

#include "verilated.h"
#include "verilated_vcd_c.h"

// INCLUDE MODEL CLASS

#include "Vff_top.h"

// INCLUDE MODULE CLASSES
#include "Vff_top___024root.h"
#include "Vff_top___024unit.h"
#include "Vff_top_ff_ifc.h"
#include "Vff_top___024unit__03a__03atransaction__Vclpkg.h"
#include "Vff_top___024unit__03a__03atesting_env__Vclpkg.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES)Vff_top__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vff_top* const __Vm_modelp;
    bool __Vm_dumping = false;  // Dumping is active
    VerilatedMutex __Vm_dumperMutex;  // Protect __Vm_dumperp
    VerilatedVcdC* __Vm_dumperp VL_GUARDED_BY(__Vm_dumperMutex) = nullptr;  /// Trace class for $dump*
    bool __Vm_activity = false;  ///< Used by trace routines to determine change occurred
    uint32_t __Vm_baseCode = 0;  ///< Used by trace routines when tracing multiple models
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vff_top___024root              TOP;
    Vff_top___024unit__03a__03atesting_env__Vclpkg TOP____024unit__03a__03atesting_env__Vclpkg;
    Vff_top___024unit__03a__03atransaction__Vclpkg TOP____024unit__03a__03atransaction__Vclpkg;
    Vff_top___024unit              TOP____024unit;
    Vff_top_ff_ifc                 TOP__ff_top__DOT__IFC;

    // SCOPE NAMES
    VerilatedScope __Vscope_ff_top__bench;

    // CONSTRUCTORS
    Vff_top__Syms(VerilatedContext* contextp, const char* namep, Vff_top* modelp);
    ~Vff_top__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
    void _traceDump();
    void _traceDumpOpen();
    void _traceDumpClose();
};

#endif  // guard
