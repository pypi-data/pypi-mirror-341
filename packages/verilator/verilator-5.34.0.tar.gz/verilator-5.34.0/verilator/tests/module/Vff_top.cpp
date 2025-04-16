// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vff_top__pch.h"
#include "verilated_vcd_c.h"

//============================================================
// Constructors

Vff_top::Vff_top(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vff_top__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , __PVT____024unit{vlSymsp->TOP.__PVT____024unit}
    , __PVT__ff_top__DOT__IFC{vlSymsp->TOP.__PVT__ff_top__DOT__IFC}
    , __024unit__03a__03atransaction__Vclpkg{vlSymsp->TOP.__024unit__03a__03atransaction__Vclpkg}
    , __024unit__03a__03atesting_env__Vclpkg{vlSymsp->TOP.__024unit__03a__03atesting_env__Vclpkg}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
    contextp()->traceBaseModelCbAdd(
        [this](VerilatedTraceBaseC* tfp, int levels, int options) { traceBaseModel(tfp, levels, options); });
}

Vff_top::Vff_top(const char* _vcname__)
    : Vff_top(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vff_top::~Vff_top() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vff_top___024root___eval_debug_assertions(Vff_top___024root* vlSelf);
#endif  // VL_DEBUG
void Vff_top___024root___eval_static(Vff_top___024root* vlSelf);
void Vff_top___024root___eval_initial(Vff_top___024root* vlSelf);
void Vff_top___024root___eval_settle(Vff_top___024root* vlSelf);
void Vff_top___024root___eval(Vff_top___024root* vlSelf);

void Vff_top::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vff_top::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vff_top___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_activity = true;
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vff_top___024root___eval_static(&(vlSymsp->TOP));
        Vff_top___024root___eval_initial(&(vlSymsp->TOP));
        Vff_top___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vff_top___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

void Vff_top::eval_end_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+eval_end_step Vff_top::eval_end_step\n"); );
#ifdef VM_TRACE
    // Tracing
    if (VL_UNLIKELY(vlSymsp->__Vm_dumping)) vlSymsp->_traceDump();
#endif  // VM_TRACE
}

//============================================================
// Events and timing
bool Vff_top::eventsPending() { return false; }

uint64_t Vff_top::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vff_top::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vff_top___024root___eval_final(Vff_top___024root* vlSelf);

VL_ATTR_COLD void Vff_top::final() {
    Vff_top___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vff_top::hierName() const { return vlSymsp->name(); }
const char* Vff_top::modelName() const { return "Vff_top"; }
unsigned Vff_top::threads() const { return 1; }
void Vff_top::prepareClone() const { contextp()->prepareClone(); }
void Vff_top::atClone() const {
    contextp()->threadPoolpOnClone();
}
std::unique_ptr<VerilatedTraceConfig> Vff_top::traceConfig() const {
    return std::unique_ptr<VerilatedTraceConfig>{new VerilatedTraceConfig{false, false, false}};
};

//============================================================
// Trace configuration

void Vff_top___024root__trace_decl_types(VerilatedVcd* tracep);

void Vff_top___024root__trace_init_top(Vff_top___024root* vlSelf, VerilatedVcd* tracep);

VL_ATTR_COLD static void trace_init(void* voidSelf, VerilatedVcd* tracep, uint32_t code) {
    // Callback from tracep->open()
    Vff_top___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vff_top___024root*>(voidSelf);
    Vff_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    if (!vlSymsp->_vm_contextp__->calcUnusedSigs()) {
        VL_FATAL_MT(__FILE__, __LINE__, __FILE__,
            "Turning on wave traces requires Verilated::traceEverOn(true) call before time 0.");
    }
    vlSymsp->__Vm_baseCode = code;
    tracep->pushPrefix(std::string{vlSymsp->name()}, VerilatedTracePrefixType::SCOPE_MODULE);
    Vff_top___024root__trace_decl_types(tracep);
    Vff_top___024root__trace_init_top(vlSelf, tracep);
    tracep->popPrefix();
}

VL_ATTR_COLD void Vff_top___024root__trace_register(Vff_top___024root* vlSelf, VerilatedVcd* tracep);

VL_ATTR_COLD void Vff_top::traceBaseModel(VerilatedTraceBaseC* tfp, int levels, int options) {
    (void)levels; (void)options;
    VerilatedVcdC* const stfp = dynamic_cast<VerilatedVcdC*>(tfp);
    if (VL_UNLIKELY(!stfp)) {
        vl_fatal(__FILE__, __LINE__, __FILE__,"'Vff_top::trace()' called on non-VerilatedVcdC object;"
            " use --trace-fst with VerilatedFst object, and --trace with VerilatedVcd object");
    }
    stfp->spTrace()->addModel(this);
    stfp->spTrace()->addInitCb(&trace_init, &(vlSymsp->TOP));
    Vff_top___024root__trace_register(&(vlSymsp->TOP), stfp->spTrace());
}
