// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vff_top__pch.h"
#include "Vff_top.h"
#include "Vff_top___024root.h"
#include "Vff_top___024unit.h"
#include "Vff_top_ff_ifc.h"
#include "Vff_top___024unit__03a__03atransaction__Vclpkg.h"
#include "Vff_top___024unit__03a__03atesting_env__Vclpkg.h"

// FUNCTIONS
Vff_top__Syms::~Vff_top__Syms()
{
#ifdef VM_TRACE
    if (__Vm_dumping) _traceDumpClose();
#endif  // VM_TRACE
}

void Vff_top__Syms::_traceDump() {
    const VerilatedLockGuard lock(__Vm_dumperMutex);
    __Vm_dumperp->dump(VL_TIME_Q());
}

void Vff_top__Syms::_traceDumpOpen() {
    const VerilatedLockGuard lock(__Vm_dumperMutex);
    if (VL_UNLIKELY(!__Vm_dumperp)) {
        __Vm_dumperp = new VerilatedVcdC();
        __Vm_modelp->trace(__Vm_dumperp, 0, 0);
        std::string dumpfile = _vm_contextp__->dumpfileCheck();
        __Vm_dumperp->open(dumpfile.c_str());
        __Vm_dumping = true;
    }
}

void Vff_top__Syms::_traceDumpClose() {
    const VerilatedLockGuard lock(__Vm_dumperMutex);
    __Vm_dumping = false;
    VL_DO_CLEAR(delete __Vm_dumperp, __Vm_dumperp = nullptr);
}

Vff_top__Syms::Vff_top__Syms(VerilatedContext* contextp, const char* namep, Vff_top* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
    , TOP____024unit__03a__03atesting_env__Vclpkg{this, Verilated::catName(namep, "$unit::testing_env__Vclpkg")}
    , TOP____024unit__03a__03atransaction__Vclpkg{this, Verilated::catName(namep, "$unit::transaction__Vclpkg")}
    , TOP____024unit{this, Verilated::catName(namep, "$unit")}
    , TOP__ff_top__DOT__IFC{this, Verilated::catName(namep, "ff_top.IFC")}
{
        // Check resources
        Verilated::stackCheck(133);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-9);
    // Setup each module's pointers to their submodules
    TOP.__024unit__03a__03atesting_env__Vclpkg = &TOP____024unit__03a__03atesting_env__Vclpkg;
    TOP.__024unit__03a__03atransaction__Vclpkg = &TOP____024unit__03a__03atransaction__Vclpkg;
    TOP.__PVT____024unit = &TOP____024unit;
    TOP.__PVT__ff_top__DOT__IFC = &TOP__ff_top__DOT__IFC;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    TOP____024unit__03a__03atesting_env__Vclpkg.__Vconfigure(true);
    TOP____024unit__03a__03atransaction__Vclpkg.__Vconfigure(true);
    TOP____024unit.__Vconfigure(true);
    TOP__ff_top__DOT__IFC.__Vconfigure(true);
    // Setup scopes
    __Vscope_ff_top__bench.configure(this, name(), "ff_top.bench", "bench", "<null>", -9, VerilatedScope::SCOPE_OTHER);
    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
    }
}
