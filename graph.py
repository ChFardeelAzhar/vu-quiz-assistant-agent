from langgraph.graph import StateGraph, START, END
from state import AgentState
import os
import subprocess
from dotenv import load_dotenv
# .env file ko load karne ke liye
load_dotenv()

from browser_service import browser_service

# ==========================================
# 1. NODES (Ye functions actual kaam karenge)
# ==========================================

def portal_manager_node(state: AgentState):
    print("-> Portal Manager Node Called: Logging into VU Portal (via Playwright)...")
    
    # .env file se ID aur Password uthana
    vu_id = os.getenv("VU_ID", "")
    vu_pass = os.getenv("VU_PASSWORD", "")
    
    if not vu_id or not vu_pass:
        print("ERROR: VU_ID ya VU_PASSWORD .env file mein nahi mila!")
        return {"portal_status": "error"}

    try:
        # Browser start karo
        browser_service.start_browser()
        
        # Login karo
        browser_service.login_to_vu(vu_id, vu_pass)
        
        # Quizzes extract karo (Next step mein implement hoga)
        quizzes = browser_service.get_pending_quizzes()
        
        return {"portal_status": "logged_in", "pending_quizzes": quizzes}
    except Exception as e:
        print("Browser Error:", str(e))
        return {"portal_status": "error"}


def quiz_supervisor_node(state: AgentState):
    print("-> Quiz Supervisor Node Called: Deciding next step...")
    # Supervisor sirf graph ki state dekhta hai, usay update nahi karta
    return state 

def quiz_solver_node(state: AgentState):
    print("-> Quiz Solver Node Called: Attempting Quiz with AI...")
    # Yahan AI aayega, quiz solve karega aur pending list me se wo quiz nikal dega
    remaining_quizzes = state.pending_quizzes[1:] # Pehli nikal di
    return {"current_quiz_status": "completed", "pending_quizzes": remaining_quizzes}

def email_notifier_node(state: AgentState):
    print("-> Email Notifier Node Called: Sending Report via Resend...")
    # Yahan Email bhejne ka code aayega
    return state

# ==========================================
# 2. CONDITIONAL EDGES (Faisla karne wala function)
# ==========================================

def should_continue(state: AgentState) -> str:
    # Agar list mein quizzes baqi hain, to solve karo
    if len(state.pending_quizzes) > 0:
        return "solve_quiz"
    # Agar list khali ho gayi hai (sab quizzes attempt ho gaye), to email bhejo
    else:
        return "send_email"


# ==========================================
# 3. BUILD THE GRAPH (Sab ko apas mein jorna)
# ==========================================

# Graph start karo AgentState ke sath
workflow = StateGraph(AgentState)

# Nodes Graph mein add karo
workflow.add_node("portal_manager", portal_manager_node)
workflow.add_node("quiz_supervisor", quiz_supervisor_node)
workflow.add_node("quiz_solver", quiz_solver_node)
workflow.add_node("email_notifier", email_notifier_node)

# Flow define karo (Kahan se kahan jana hai)
workflow.add_edge(START, "portal_manager")
workflow.add_edge("portal_manager", "quiz_supervisor")

# Supervisor se Conditional Edge (Decision)
workflow.add_conditional_edges(
    "quiz_supervisor", # Start Point
    should_continue,   # Decision wala logic function
    {
        # Function jo return kare ga : Wo kis Node par jaye ga
        "solve_quiz": "quiz_solver",
        "send_email": "email_notifier"
    }
)

# Jab quiz solve ho jaye to wapis Supervisor ke paas jao (check karne ke liye ke mazeed to nahi)
workflow.add_edge("quiz_solver", "quiz_supervisor")

# Email bhejne ke baad Graph ko End (khatam) kar do
workflow.add_edge("email_notifier", END)

# Graph ko Tayaar (Compile) karo
app = workflow.compile()