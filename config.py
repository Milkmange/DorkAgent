import sys, os, getpass

from dotenv import load_dotenv
from crewai import LLM
from langchain_openai import ChatOpenAI

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")

def read_env_file(path: str) -> dict:
    """Load key-value pairs from the .env file."""

    data = {}

    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        data[k.strip()] = v.strip()
        except Exception:
            pass

    return data

def write_env_file(path: str, values: dict):
    """Persist environment variables to the .env file."""

    existing = read_env_file(path)
    existing.update(values)
    lines = [f"{k}={existing[k]}" for k in sorted(existing.keys())]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def ensure_api_keys(llm_type: str):
    """Prompt for and store missing API keys."""

    required_keys = ["SERPER_API_KEY"]

    if llm_type == "openai":
        required_keys.append("OPENAI_API_KEY")
    elif llm_type == "anthropic":
        required_keys.append("ANTHROPIC_API_KEY")
    elif llm_type == "gemini":
        required_keys.append("GEMINI_API_KEY")

    missing = [k for k in required_keys if not os.getenv(k)]

    if missing:
        print("[!] Missing required API keys: " + ", ".join(missing))
        provided = {}
        for key in missing:
            prompt_text = f"Enter value for {key}: "
            try:
                val = getpass.getpass(prompt_text)
            except Exception:
                val = input(prompt_text)
            provided[key] = val.strip()
        write_env_file(ENV_PATH, provided)
        load_dotenv(dotenv_path=ENV_PATH, override=True)

def verify_api_key(llm_type: str):
    """Verify required API keys are set."""

    required_keys = ["SERPER_API_KEY"]

    if llm_type == "openai":
        required_keys.append("OPENAI_API_KEY")
    elif llm_type == "anthropic":
        required_keys.append("ANTHROPIC_API_KEY")
    elif llm_type == "gemini":
        required_keys.append("GEMINI_API_KEY")

    load_dotenv()

    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print("[!] Missing required API keys:")
        for key in missing_keys:
            print(f"    - {key} is not set")
        print("\nPlease check your .env file and set the missing keys.")
        sys.exit(1)

def select_llm_type():
    """Select LLM type for agents."""

    while True:
        print("\n")
        print("1. GPT-4.1 Mini")
        print("2. Claude 3.5 Haiku")
        print("3. Gemini 2.0 Flash")
        print("\n")

        choice = input("[?] Choose LLM for Agents (1 - 3): ").strip()

        if choice == "1":
            return "openai"
        elif choice == "2":
            return "anthropic"
        elif choice == "3":
            return "gemini"
        else:
            print("[!] Invalid choice. Please enter 1 - 3.")

def create_llm(llm_type):
    """Create LLM instance based on type."""

    if llm_type == "openai":
        return ChatOpenAI(
            model_name="gpt-4.1-mini-2025-04-14",
        )
    elif llm_type == "anthropic":
        return LLM(
            api_key=os.getenv('ANTHROPIC_API_KEY'),
            model='anthropic/claude-3-5-haiku-20241022',
        )
    elif llm_type == "gemini":
        return LLM(
            api_key=os.getenv('GEMINI_API_KEY'),
            model='gemini/gemini-2.5-flash',
        )
    else:
        raise ValueError(f"Unknown LLM type: {llm_type}")