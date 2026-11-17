"""Optional Gemini narration helper. The app remains usable without an API key."""
import os
from dotenv import load_dotenv

load_dotenv()

def generate_reply(messages: list[dict[str, str]], system_prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "The library is silent except for the ticking clock. I can still guide "
            "the adventure in demo mode. Add GEMINI_API_KEY to your .env file to "
            "enable Gemini-powered narration. " + _fallback(messages[-1]["content"] if messages else "")
        )
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        transcript = "\n".join(
            f'{m["role"].upper()}: {m["content"]}' for m in messages[-12:]
        )
        response = client.models.generate_content(
            model=model,
            contents=f"{system_prompt}\n\nConversation:\n{transcript}\n\nGAME MASTER:"
        )
        return response.text or "A strange silence fills the library. Try another action."
    except Exception as exc:
        return f"[Gemini connection issue: {type(exc).__name__}. Continuing in demo mode.] " + _fallback(
            messages[-1]["content"] if messages else ""
        )

def _fallback(message: str) -> str:
    msg = message.lower()
    if "desk" in msg:
        return "You search the desk and discover a small brass key beneath a folded map."
    if "bookshelf" in msg or "books" in msg:
        return "Four books are out of alignment. Their spines read KEY, LIGHT, IMAGE, EXIT."
    if "drawer" in msg:
        return "The drawer is locked. Something small and metallic may fit its keyhole."
    if "painting" in msg:
        return "The painting depicts a night sky. Its surface seems to conceal something."
    if "globe" in msg:
        return "A tiny inscription reads: Not every message is visible in ordinary light."
    if "4179" in msg:
        return "The keypad flashes green. The door opens. You escaped!"
    return "Dust drifts through the moonlight. Examine the desk, bookshelf, painting, drawer or globe to continue."


def narrate_validated_result(validated_result: str) -> str:
    """Optionally add atmosphere without changing the Python-validated outcome."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return validated_result
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model,
            contents=(
                "You narrate a text escape-room game. Rewrite the following already-validated "
                "game outcome in a vivid but concise style. Preserve every fact exactly. "
                "Do not invent items, clues, state changes, codes, permissions or success. "
                "Do not add any new game action. Validated outcome: " + validated_result
            )
        )
        return response.text or validated_result
    except Exception:
        return validated_result
