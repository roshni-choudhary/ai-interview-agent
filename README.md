<div align="center">
  <h1>🐅 The Furious Five of Hiring: Agentic AI Interviewer</h1>
  <p><strong>A fully autonomous, pair-programming AI interviewer for System Design, DSA, and Aptitude.</strong></p>
</div>

---

## 🛑 The Problem with Tech Hiring Today
Let's be real: technical hiring is broken. 
1. **Take-home assignments** are instantly solved by ChatGPT.
2. **Static platforms (like LeetCode)** just test if the code passes a unit test. They don't test communication, problem-solving under pressure, or architectural thinking.
3. **Manual interviews** drain thousands of hours of expensive senior engineering time.

## 🚀 What We Built
This isn't just a chatbot wrapping an LLM. This is an **Agentic AI Interviewer** that acts as a true sparring partner. It runs your code, analyzes your architectural choices, and guides you through complex problems just like a human Grandmaster would. 

Instead of just checking for correct answers, our agent evaluates the *process*. 

### 🏆 The 3 Pillars of Evaluation:
1. **System Design (The Architecture of Empires)** 🏛️
   - Engages in deep-dive architectural discussions.
   - Evaluates scalability, database choices, load balancing, and bottlenecks.
   - Pushes back on bad design decisions to test the candidate's reasoning.
2. **DSA & Live Coding (The Iron Fortress Sandbox)** 💻
   - Integrated browser IDE with a secure, isolated Docker backend.
   - If the code fails, the AI *reads the stack trace* and provides Socratic hints (not direct answers!) to guide the candidate's logic.
3. **Aptitude & Logical Reasoning (The Inner Chi)** 🧠
   - Adaptive questioning that adjusts difficulty based on the candidate's real-time performance.
   - Evaluates communication clarity and analytical thinking.

## 🛠️ The Tech Stack (Weapons of the Dojo)
We built a highly scalable, isolated, and stateful architecture to make this work:

* **Frontend:** React, Vite, TailwindCSS (Providing a fluid, side-by-side IDE and chat interface)
* **Backend:** Python, FastAPI, WebSockets (For real-time streaming and execution)
* **AI Orchestration:** LangGraph, OpenAI GPT-4o (Stateful, multi-agent reasoning loops)
* **Code Sandbox Environment:** Docker, Judge0, Pytest (For 100% secure, isolated code execution)

## 🧠 How the Agentic Workflow Operates
Unlike a standard LLM call, our AI operates on a state machine powered by **LangGraph**:
1. **Submission:** The candidate submits unverified code or a system design diagram.
2. **Execution:** The backend spins up an isolated sandbox and runs the code against hidden edge cases.
3. **Analysis:** The Agent intercepts the `stdout` and stack traces.
4. **Reasoning Loop:** LangGraph determines the logical flaw (e.g., "They used an O(n^2) approach instead of a Hash Map").
5. **Guidance:** The AI generates a contextual hint and evaluates the candidate's time/space complexity.

## ⚙️ Running the Dojo Locally

### Prerequisites
* Python 3.10+
* Node.js & npm
* Docker (must be running for the code sandbox)

### Setup Instructions
1. **Clone the repo:**
   ```bash
   git clone https://github.com/roshni-choudhary/ai-interview-agent.git
   cd ai-interview-agent
   ```
2. **Start the Sandbox & Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Set your OPENAI_API_KEY in a .env file
   uvicorn main:app --reload
   ```
3. **Start the Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
4. **Enter the Dojo:** Open `http://localhost:5173` in your browser.

## 🔮 Future Roadmap (The Path to Mastery)
- [ ] **Phase 1:** Real-time WebRTC Voice interactions (The AI physically speaks to you).
- [ ] **Phase 2:** Multi-language support (C++, Rust, Go).
- [ ] **Phase 3:** Enterprise dashboard for recruiters to view detailed evaluation reports.

---
*Built with ❤️ for the Agentic AI & Automation Track.*
