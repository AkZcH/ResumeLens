SKILL_KEYWORDS = {
    "python": ["python", "py"],
    "javascript": ["javascript", "js", "node.js", "nodejs"],
    "react": ["react", "react.js", "reactjs"],
    "sql": ["sql", "postgres", "postgresql", "mysql"],
    "java": ["java"],
    "cpp": ["c++", "cpp"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker", "containerization"],
    "fastapi": ["fastapi", "fast api"],
    "django": ["django"],
    "flask": ["flask"],
    "git": ["git", "github", "gitlab"],
    "linux": ["linux", "unix"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],
    "kubernetes": ["kubernetes", "k8s"]
}

def get_all_skills():
    """Get flattened list of all skills."""
    skills = []
    for skill_variants in SKILL_KEYWORDS.values():
        skills.extend(skill_variants)
    return skills