```markdown
# 🦷 Dental Clinic Voice Assistant

This project is an **AI-powered FastAPI application** that simulates a voice/chat assistant for a dental clinic.  
It allows users to interact with the clinic, manage appointments, and query available slots via a natural language interface.

---

## Features
- **Chat API**: AI-based chat endpoint (`/chat/completions`) with tool-call support
- **Appointments Management**: Create, check, reschedule, and cancel appointments
- **Available Slots**: Query available service slots
- **Streaming Responses**: Real-time AI output via Server-Sent Events (SSE)

---

## Project Structure

```

project-root/
├─ api/
│  ├─ routes.py          # FastAPI router definitions (endpoints only)
│  ├─ chat\_logic.py      # Chat request handling and streaming logic
│  ├─ tool\_handler.py    # Dispatcher for tool calls (appointments, slots)
│  └─ utils.py           # Helper functions (e.g., load clinic info)
├─ core/
│  └─ config.py          # MongoDB and OpenAI client configuration
├─ services/
│  └─ ...                # Business logic for appointments and slots
├─ clinic\_info.txt       # Clinic information used as system prompt context
├─ main.py               # FastAPI application entrypoint
├─ requirements.txt      # Python dependencies
├─ .env.example          # Example environment variables
├─ .gitignore            # Files to ignore in git
└─ README.md

````

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/voice-agent-project.git
cd voice-agent-project
````

### 2. Create a Virtual Environment

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URI=mongodb://localhost:27017
OPENAI_API_KEY=your-openai-api-key
```

> If you do not have an OpenAI key, the app can still run but AI-powered endpoints will return mock responses or errors.

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Setting Up VAPI

To use this project with **Voice AI Platform (VAPI)**:

1. **Create a VAPI Account**  
   - Go to [VAPI Sign Up](https://vapi.example.com/signup) and create an account.
   - Verify your email and log in.

2. **Create a New Assistant / Voice Project**  
   - After logging in, create a new project and select a voice assistant template.

3. **Add the Prompt**  
   - Copy the contents of `VAPI_PROMPT.md` or the **Hana Assistant Prompt** (see below) and paste it into the assistant’s prompt/input section in the VAPI panel.  
   - This ensures your voice assistant uses the correct persona, flows, and behavior.

4. **Configure API / Webhook (Optional)**  
   - If you want the VAPI assistant to call your FastAPI endpoints, configure the webhook URL to point to your `/chat/completions` endpoint.

---
## Usage

### Chat Completions Endpoint

```
POST /chat/completions
```

* **Request Body**: JSON containing `messages`, `model`, `temperature`, `max_tokens`, etc.
* **Response**: Streaming AI response (Server-Sent Events)

Example with `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini", 
    "messages": [{"role":"user","content":"I want to book a dental appointment tomorrow morning."}],
    "temperature": 0.2,
    "max_tokens": 500
  }'
```

> Note: Streaming requires SSE-compatible clients to properly receive real-time chunks.

---

## Notes

* The application uses **async MongoDB (Motor)** to ensure high concurrency.
* `lifespan` events are used for startup/shutdown tasks, like creating database indexes.
* `clinic_info.txt` provides context to the AI model for helpful responses.
* The project separates **endpoint routing, chat logic, and tool handling** for maintainability and clean structure.

---

## Environment Variables

* `MONGODB_URI`: MongoDB connection string
* `OPENAI_API_KEY`: OpenAI API key (for AI completions)

```
