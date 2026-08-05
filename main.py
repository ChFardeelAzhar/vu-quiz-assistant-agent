from graph import app

def run_agent():
    print("🚀 Starting VU Quiz Agent...\n")
    
    # 1. Initial State: Jab agent start hoga to sab kuch khali hoga
    initial_state = {
        "messages": [],
        "portal_status": "logged_out",
        "pending_quizzes": [],
        "current_quiz_status": "none",
        "quiz_results": []
    }

    # 2. Graph ko Invoke/Run karna
    # `app.stream` ka faida ye hai ke ye har step ke baad ruk kar output dikhata hai
    for output in app.stream(initial_state):
        # Har node jab apna kaam khatam karta hai, to wo yahan print hoga
        for node_name, state_update in output.items():
            print(f"\n✅ Finished Node: [{node_name}]")
            print(f"State Update: {state_update}")
            print("-" * 50)

if __name__ == "__main__":
    run_agent()