# How Your Country AI Agent Works

This guide explains how this tool handles your questions using a structured, step-by-step process. This design ensures that every answer is grounded in real facts rather than AI guesses.

## The Path of Your Question

When you ask a question like *"What is the population of India?"*, it follows a clear three-step path:

### Step 1: Understanding Your Intent
First, the agent acts like a **Detective**. 
- It identifies which country you are asking about (e.g., India).
- It identifies exactly what data you need (e.g., Population).
- If you ask something unrelated to countries, it will politely tell you it’s a specialist and can’t help with other topics.

### Step 2: Gathering the Facts
Once the country is identified, the agent acts like a **Researcher**.
- It reaches out to an official digital library (the REST Countries API) to get the most accurate, live data.
- It is programmed to handle minor network hiccups by retrying automatically, so you don't have to worry about simple connection errors.

### Step 3: Writing the Reply
Finally, the agent acts like a **Professional Writer**.
- It takes the raw facts gathered in the research step.
- It writes a clean, friendly response for you in Markdown format.
- **Important**: It is strictly forbidden from making up facts. If it can't find the info in the library, it will tell you honestly.

---

## Technical Architecture (The 3-Node Workflow)
This agent is built as a **Manual StateGraph** using LangGraph. This means we have explicit control over each phase:

1.  **Intent / Field Identification Node**: Extracting structured data.
2.  **Tool Invocation Node**: Securely fetching data.
3.  **Answer Synthesis Node**: Writing the grounded response.

---
*Created by your Antigravity AI assistant*
