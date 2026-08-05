from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
import operator

class AgentState(TypedDict):
    # Chat/Log history
    messages: Annotated[list, add_messages]
    
    # Custom States 
    portal_status: str
    
    # --- New Architecture States for ASP.NET PostBack Loop ---
    courses: List[Dict[str, Any]]
    currentCourseIndex: int
    quizData: Dict[str, List[Dict[str, Any]]]
    pending_quizzes_summary: Dict[str, Any]
    # ---------------------------------------------------------

    pending_quizzes: List[Dict[str, Any]]
    current_quiz_status: str
    quiz_results: List[Dict[str, Any]]