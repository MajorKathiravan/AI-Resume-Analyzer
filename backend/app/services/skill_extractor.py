import re


SKILL_PATTERNS = {
    # =========================
    # Programming Languages
    # =========================
    "python": r"\bpython\b",
    "java": r"\bjava\b",
    "javascript": r"\bjavascript\b",
    "typescript": r"\btypescript\b",
    "sql": r"\bsql\b",

    # =========================
    # Web Development
    # =========================
    "html": r"\bhtml\b",
    "css": r"\bcss\b",
    "react": r"\breact(?:\.js)?\b",
    "node.js": r"\bnode(?:\.js)?\b",
    "fastapi": r"\bfastapi\b",
    "flask": r"\bflask\b",
    "django": r"\bdjango\b",

    # =========================
    # APIs
    # =========================
    "api": r"\bapi\b",
    "rest api": r"\brest(?:ful)?\s+api\b",
    "graphql": r"\bgraphql\b",

    # =========================
    # Databases
    # =========================
    "mysql": r"\bmysql\b",
    "postgresql": r"\bpostgresql\b|\bpostgres\b",
    "mongodb": r"\bmongodb\b",
    "redis": r"\bredis\b",
    "sqlite": r"\bsqlite\b",

    # =========================
    # Data Science
    # =========================
    "pandas": r"\bpandas\b",
    "numpy": r"\bnumpy\b",
    "matplotlib": r"\bmatplotlib\b",
    "seaborn": r"\bseaborn\b",
    "power bi": r"\bpower\s*bi\b",
    "tableau": r"\btableau\b",

    # =========================
    # Machine Learning / AI
    # =========================
    "machine learning": r"\bmachine\s+learning\b",
    "deep learning": r"\bdeep\s+learning\b",
    "artificial intelligence": r"\bartificial\s+intelligence\b|\bai\b",
    "natural language processing": r"\bnatural\s+language\s+processing\b",
    "nlp": r"\bnlp\b",
    "computer vision": r"\bcomputer\s+vision\b",
    "reinforcement learning": r"\breinforcement\s+learning\b",

    # =========================
    # AI Frameworks
    # =========================
    "tensorflow": r"\btensorflow\b",
    "pytorch": r"\bpytorch\b",
    "scikit-learn": r"\bscikit[\s-]?learn\b",
    "transformers": r"\btransformers\b",
    "sentence transformers": r"\bsentence\s+transformers\b",

    # =========================
    # Generative AI / LLM
    # =========================
    "llm": r"\bllm(?:s)?\b|\blarge\s+language\s+models?\b",
    "generative ai": r"\bgenerative\s+ai\b",
    "rag": r"\brag\b|\bretrieval[\s-]augmented\s+generation\b",
    "langchain": r"\blangchain\b",
    "ollama": r"\bollama\b",
    "openai": r"\bopenai\b",
    "prompt engineering": r"\bprompt\s+engineering\b",
    "fine-tuning": r"\bfine[\s-]?tuning\b",
    "embeddings": r"\bembeddings?\b",
    "vector database": r"\bvector\s+databases?\b",

    # =========================
    # Cloud
    # =========================
    "aws": r"\baws\b|\bamazon\s+web\s+services\b",
    "azure": r"\bazure\b|\bmicrosoft\s+azure\b",
    "gcp": r"\bgcp\b|\bgoogle\s+cloud\b",
    "cloud computing": r"\bcloud\s+computing\b",
    "bigquery": r"\bbigquery\b",

    # =========================
    # DevOps / Infrastructure
    # =========================
    "docker": r"\bdocker\b",
    "kubernetes": r"\bkubernetes\b|\bk8s\b",
    "git": r"\bgit\b",
    "github": r"\bgithub\b",
    "ci/cd": r"\bci\s*/\s*cd\b|\bcontinuous\s+integration\b|\bcontinuous\s+deployment\b",
    "linux": r"\blinux\b",

    # =========================
    # Data Engineering
    # =========================
    "data processing": r"\bdata\s+processing\b",
    "data analysis": r"\bdata\s+analysis\b",
    "data visualization": r"\bdata\s+visualization\b",
    "data cleaning": r"\bdata\s+cleaning\b",
    "etl": r"\betl\b|\bextract[\s-]+transform[\s-]+load\b",
    "apache spark": r"\bapache\s+spark\b|\bspark\b",
    "airflow": r"\bairflow\b",

    # =========================
    # Automation / Product
    # =========================
    "automation": r"\bautomation\b",
    "rpa": r"\brpa\b|\brobotic\s+process\s+automation\b",
    "agile": r"\bagile\b",
    "rest api development": r"\brest\s+api\s+development\b",
}


def extract_skills(text: str) -> list[str]:
    """
    Extract known technical skills from text.

    Matching is case-insensitive and uses word-aware
    regular expressions to reduce false positives.
    """

    if not text:
        return []

    text_lower = text.lower()

    found_skills = []

    for skill, pattern in SKILL_PATTERNS.items():

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))