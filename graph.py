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
    print("-> Portal Manager Node Called: Logging in and extracting courses...")
    
    vu_id = os.getenv("VU_ID", "")
    vu_pass = os.getenv("VU_PASSWORD", "")
    
    if not vu_id or not vu_pass:
        print("ERROR: VU_ID ya VU_PASSWORD .env file mein nahi mila!")
        return {"portal_status": "error"}

    try:
        browser_service.start_browser()
        browser_service.login_to_vu(vu_id, vu_pass)
        
        # Dashboard se courses nikalo
        courses = browser_service.extract_courses_from_dashboard()
        
        return {
            "portal_status": "logged_in", 
            "courses": courses, 
            "currentCourseIndex": 0,
            "quizData": {}
        }
    except Exception as e:
        print("Browser Error:", str(e))
        return {"portal_status": "error"}


def quiz_scraper_node(state: AgentState):
    idx = state.get("currentCourseIndex", 0)
    courses = state.get("courses", [])
    
    if idx < len(courses):
        course = courses[idx]
        print(f"-> Quiz Scraper Node: Processing course {idx+1}/{len(courses)}: {course['name']}")
        
        scraped_quizzes = browser_service.scrape_course_quizzes(course['index'], course['name'])
        
        # Naya dictionary reference banayen ta ke LangGraph update detect kare
        current_quiz_data = state.get("quizData", {}).copy()
        current_quiz_data[course['name']] = scraped_quizzes
        
        return {
            "quizData": current_quiz_data,
            "currentCourseIndex": idx + 1
        }
    return {}

def quiz_scraper_router(state: AgentState) -> str:
    # Faisla karega ke loop dubara chalana hai ya agay jana hai
    idx = state.get("currentCourseIndex", 0)
    courses = state.get("courses", [])
    if idx < len(courses):
        return "scrape_next"
    else:
        return "analyze"

def quiz_analyzer_node(state: AgentState):
    print("-> Quiz Analyzer Node Called: Computing summaries & Saving MD files...")
    
    pending = []
    attempted = []
    upcoming = []
    
    quiz_data = state.get("quizData", {})
    
    # MD Files ke liye output folder banayen
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    for course_name, quizzes in quiz_data.items():
        # Har course ke liye markdown file banana
        safe_name = "".join([c for c in course_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filepath = os.path.join(output_dir, f"{safe_name}.md")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {course_name} - Quizzes Summary\n\n")
            if not quizzes:
                f.write("> Is course ki koi quiz available nahi hai.\n")
            else:
                f.write("| # | Quiz Title | Start Date | End Date | Total Marks | Open/Close | Status | Result |\n")
                f.write("|---|---|---|---|---|---|---|---|\n")
                for q in quizzes:
                    f.write(f"| {q['number']} | {q['title']} | {q['start']} | {q['end']} | {q['totalMarks']} | {q['open_close']} | {q['status']} | {q['result']} |\n")
                    
        for quiz in quizzes:
            status = quiz["status"].lower()
            open_close = quiz["open_close"].lower()
            
            quiz_info = {
                "subject": course_name,
                "title": quiz["title"],
                "start": quiz["start"],
                "end": quiz["end"]
            }
            
            # Agar submitted hai ya result aa gaya hai, ya status 'closed' hai
            if status in ["submitted", "result declared"] or "closed" in open_close:
                attempted.append(quiz_info)
            # Agar 'open' likha hai
            elif "open" in open_close or (not status and not open_close):
                pending.append(quiz_info)
            else:
                upcoming.append(quiz_info)
                
    summary = {
        "pending": pending,
        "attempted": attempted,
        "upcoming": upcoming
    }
    
    print(f"\n✅ All courses data saved in '{output_dir}/' folder.")
    print("\n=== PENDING QUIZZES SUMMARY ===")
    import json
    print(json.dumps(summary, indent=2))
    
    return {
        "pending_quizzes_summary": summary,
        "pending_quizzes": pending
    }

def quiz_supervisor_node(state: AgentState):
    print("-> Quiz Supervisor Node Called: Deciding next step...")
    return state 

def quiz_solver_node(state: AgentState):
    print("-> Quiz Solver Node Called: Attempting Quiz with AI...")
    pending_list = state.get("pending_quizzes", [])
    remaining_quizzes = pending_list[1:] if pending_list else []
    return {"current_quiz_status": "completed", "pending_quizzes": remaining_quizzes}

def email_notifier_node(state: AgentState):
    print("-> Email Notifier Node Called: Sending Report via Resend...")
    return state

def should_continue(state: AgentState) -> str:
    pending = state.get("pending_quizzes", [])
    if len(pending) > 0:
        return "solve_quiz"
    else:
        return "send_email"

# ==========================================
# 3. BUILD THE GRAPH (Sab ko apas mein jorna)
# ==========================================

workflow = StateGraph(AgentState)

# Naye Nodes add kiye
workflow.add_node("portal_manager", portal_manager_node)
workflow.add_node("quiz_scraper", quiz_scraper_node)
workflow.add_node("quiz_analyzer", quiz_analyzer_node)
workflow.add_node("quiz_supervisor", quiz_supervisor_node)
workflow.add_node("quiz_solver", quiz_solver_node)
workflow.add_node("email_notifier", email_notifier_node)

# START -> Portal -> Scraper Loop
workflow.add_edge(START, "portal_manager")
workflow.add_edge("portal_manager", "quiz_scraper")

# Scraper se Loop nikale ga
workflow.add_conditional_edges(
    "quiz_scraper",
    quiz_scraper_router,
    {
        "scrape_next": "quiz_scraper",
        "analyze": "quiz_analyzer"
    }
)

# Analyzer ke baad Supervisor ke paas jayega
workflow.add_edge("quiz_analyzer", "quiz_supervisor")

# Supervisor se aagay (Solver ya Email)
workflow.add_conditional_edges(
    "quiz_supervisor", 
    should_continue,   
    {
        "solve_quiz": "quiz_solver",
        "send_email": "email_notifier"
    }
)

workflow.add_edge("quiz_solver", "quiz_supervisor")
workflow.add_edge("email_notifier", END)

app = workflow.compile()