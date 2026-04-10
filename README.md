# Country Intelligence Agent 

Welcome to the **Country Intelligence Agent**—your personal digital scout for everything related to the world's nations. 

Built with the latest in AI orchestration, this agent doesn't just guess facts; it performs live "research" to give you accurate, grounded information every single time. 

---

## What Makes This Agent Special?

Most AI bots rely on their memory, which can be old or just plain wrong. This agent is built differently:
- **Fact-First Approach**: It uses a dedicated "Researcher" mode to fetch live data from the **REST Countries API**.
- **Three-Step Reasoning**: Instead of one long prompt, it breaks every question down:
    1.  **The Detective**: Figures out exactly what you're looking for.
    2.  **The Researcher**: Gathers the live stats.
    3.  **The Professional Writer**: Crafts a friendly, easy-to-read reply.
- **Sleek Interface**: Wrapped in a "True Black" premium dark-mode UI that feels as fast as the AI itself.

---

## How to Get Started

Setting up your own intelligence station is easy:

1.  **Clone this space**: Download the project folder.
2.  **Add your brain power**: Open the `.env` file and paste in your `GEMINI_API_KEY`.
3.  **Install the engine**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ignition**:
    ```bash
    uvicorn app:app --reload
    ```
5.  **Go Live**: Open `index.html` in your browser and start exploring the world!

---

## Tech Behind the Scenes

This project isn't just a simple script; it's designed like a production-ready service:
- **Framework**: [LangGraph](https://github.com/langchain-ai/langgraph) (The backbone of our agent's decision-making).
- **Brain**: [Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) (Fast, efficient, and smart).
- **Back-End**: FastAPI (The high-speed highway between the AI and the screen).
- **Front-End**: Vanilla HTML/CSS (Because simple is beautiful).

---

## A Note on Privacy & Logic
This agent is a specialist. If you ask it about things besides countries (like coding or life advice), it will politely stay in its lane. It also keeps its "internal notes" (tool names) private, ensuring you only ever see the final, polished response.

*Happy exploring!* 
