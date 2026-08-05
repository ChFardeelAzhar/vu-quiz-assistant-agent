from typing import Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

# Pydantic Model (BaseModel) ka faida ye hai ke ye strict validation karta hai.
class AgentState(BaseModel):
    # Chat/Log history
    messages: Annotated[list, add_messages] = Field(default_factory=list)
    
    # Custom States 
    portal_status: str = Field(default="logged_out", description="Status of the VU portal login")
    
    # Pydantic mein hum default values de sakte hain
    pending_quizzes: List[Dict[str, Any]] = Field(default_factory=list)
    current_quiz_status: str = Field(default="none")
    quiz_results: List[Dict[str, Any]] = Field(default_factory=list)