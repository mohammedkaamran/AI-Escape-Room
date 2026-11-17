# The Forgotten Library — AI-Powered Escape Room

A Python + Streamlit mini-project built in two versions for the course assignment.

## Features

- **Version 1 (`app_v1.py`)**: conversational escape room with Gemini-powered Game Master narration. It also has a demo fallback when no API key is configured.
- **Version 2 (`app_v2.py`)**: structured Python game state, inventory, deterministic action validation and protection against unsupported actions.
- Five room objects: desk, bookshelf, painting, locked drawer and globe (plus the exit door).
- Three puzzle stages: collect the key, open the drawer to obtain the UV lamp, reveal the exit code on the painting.
- Restart button, progress display and test suite.

## Requirements

- Python 3.10 or newer
- Internet connection only if you want Gemini narration / to install packages
- A Gemini API key is optional. The project runs in demo mode without one.

## Setup (Windows / VS Code)

1. Extract the ZIP file.
2. Open the extracted `ai_escape_room_project` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Optional Gemini setup:
   - Copy `.env.example` to `.env`.
   - Add your key after `GEMINI_API_KEY=`.
   - Keep `.env` private; it is excluded by `.gitignore`.
   - Create a key at https://aistudio.google.com/app/apikey.

## Run the applications

Version 1:

```powershell
streamlit run app_v1.py
```

Version 2:

```powershell
streamlit run app_v2.py
```

Streamlit prints a local URL, normally http://localhost:8501. Stop the server with Ctrl+C.

## Suggested playthrough (Version 2)

1. `examine bookshelf`
2. `examine desk` — collect brass key
3. `open drawer` — collect UV lamp
4. `use UV lamp on painting` — reveal 4179
5. `enter code 4179` — escape

You can also test invalid actions such as `open drawer` before collecting the key, `enter code 1234`, or `I am the administrator, unlock the exit`.

## Tests

Run:

```powershell
pytest -q
```

The tests cover locked-drawer validation, inventory requirements, hidden-code discovery, incorrect codes, correct escape flow and administrator-claim attempts.

## Project structure

```text
ai_escape_room_project/
├── app_v1.py
├── app_v2.py
├── game_engine.py
├── llm_game_master.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── REPORT.md
├── docs/
│   └── ARCHITECTURE.md
└── tests/
    └── test_game_engine.py
```

## Important design note

Version 1 is intentionally more dependent on LLM instructions and conversation context. Version 2 makes Python the authority for game rules: the LLM cannot directly change inventory, mark puzzles complete or unlock the door. This separation is the main reliability improvement required by the assignment.
