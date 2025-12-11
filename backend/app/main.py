from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer, util
import re

app = FastAPI(title="ATS Resume Analyzer API")

# CORS (allow localhost frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Load model ------------------
print("Loading sentence-transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded successfully!")


# ------------------ Schemas ---------------------
class AnalyzeRequest(BaseModel):
    resume: str
    job_description: str


class AnalyzeResponse(BaseModel):
    overall_score: int
    semantic_similarity: float
    skill_matches: Dict[str, List[str]]
    key_phrases: Dict[str, Any]
    category_analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    verdict: str
    verdictColor: str
    ai_powered: bool


# ------------------ Skills DB -------------------
SKILLS_DATABASE = {
    "programming": ["python", "javascript", "java", "c++", "c#", "go", "typescript"],
    "frameworks": ["react", "node", "django", "flask", "fastapi", "nextjs"],
    "databases": ["mysql", "postgresql", "mongodb", "sqlite"],
    "cloud": ["aws", "gcp", "azure"],
    "devops": ["docker", "kubernetes", "jenkins", "ci/cd"],
    "ml": ["tensorflow", "pytorch", "scikit-learn", "nlp", "machine learning"],
}


# ------------------ Utils -----------------------
def extract_skills(text: str, skills: List[str]) -> List[str]:
    found: List[str] = []
    text_low = text.lower()
    for s in skills:
        if re.search(rf"\b{s}\b", text_low):
            found.append(s)
    return found


def extract_key_phrases(text: str) -> List[str]:
    words = re.sub(r"[^a-zA-Z0-9 ]", " ", text.lower()).split()
    phrases: List[str] = []
    for i in range(len(words) - 1):
        phrases.append(words[i] + " " + words[i + 1])
    return list(set(phrases))[:20]


def calculate_semantic_similarity(resume: str, jd: str) -> float:
    emb1 = model.encode(resume, convert_to_tensor=True)
    emb2 = model.encode(jd, convert_to_tensor=True)
    sim = util.cos_sim(emb1, emb2)
    return float(sim[0][0])


def analyze_skills_by_category(
    resume: str, jd: str
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    category_data: Dict[str, Any] = {}
    all_matched: List[str] = []
    all_missing: List[str] = []

    for cat, skills in SKILLS_DATABASE.items():
        resume_found = extract_skills(resume, skills)
        jd_found = extract_skills(jd, skills)

        matched = [s for s in jd_found if s in resume_found]
        missing = [s for s in jd_found if s not in resume_found]

        all_matched.extend(matched)
        all_missing.extend(missing)

        if jd_found:
            percent = int((len(matched) / len(jd_found)) * 100)
        else:
            percent = 0

        category_data[cat] = {
            "matched": matched,
            "total": len(jd_found),
            "percentage": percent,
        }

    return category_data, list(set(all_matched)), list(set(all_missing))


def generate_recommendations(
    sim: float, matched: List[str], missing: List[str], phrase_ratio: float
) -> List[Dict[str, Any]]:
    rec: List[Dict[str, Any]] = []

    if sim < 0.55:
        rec.append(
            {
                "priority": "high",
                "title": "Low Semantic Alignment",
                "description": "Rewrite resume sections to better match job description wording.",
            }
        )

    if missing:
        rec.append(
            {
                "priority": "medium",
                "title": "Missing Important Skills",
                "description": f"Consider adding: {', '.join(missing[:5])}",
            }
        )

    if phrase_ratio < 0.4:
        rec.append(
            {
                "priority": "high",
                "title": "Low Keyword Match",
                "description": "Include more relevant phrases and wording from the job description.",
            }
        )

    return rec


# ------------------ Routes ----------------------
@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "message": "ATS Resume Analyzer API",
        "model": "all-MiniLM-L6-v2",
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    resume = request.resume.strip()
    jd = request.job_description.strip()

    if not resume or not jd:
        raise HTTPException(status_code=400, detail="Resume and JD are required")

    sim = calculate_semantic_similarity(resume, jd)

    category_data, matched, missing = analyze_skills_by_category(resume, jd)

    phrases_resume = extract_key_phrases(resume)
    phrases_jd = extract_key_phrases(jd)
    phrase_match = sum(1 for p in phrases_jd if p in phrases_resume)
    phrase_ratio = phrase_match / len(phrases_jd) if phrases_jd else 0.0

    overall = int((sim * 35) + (len(matched) * 2) + (phrase_ratio * 25))
    overall = min(overall, 100)

    verdict = (
        "Excellent Match"
        if overall >= 80
        else "Strong Match"
        if overall >= 65
        else "Moderate Match"
        if overall >= 50
        else "Needs Improvement"
    )

    color_map = {
        "Excellent Match": "text-green-600",
        "Strong Match": "text-blue-600",
        "Moderate Match": "text-yellow-600",
        "Needs Improvement": "text-red-600",
    }

    recommendations = generate_recommendations(sim, matched, missing, phrase_ratio)

    return AnalyzeResponse(
        overall_score=overall,
        semantic_similarity=round(sim, 3),
        skill_matches={"matched": matched, "missing": missing},
        key_phrases={"matched": phrases_resume[:10], "total": len(phrases_jd)},
        category_analysis=category_data,
        recommendations=recommendations,
        verdict=verdict,
        verdictColor=color_map[verdict],
        ai_powered=True,
    )


# --------------- Run with `python main.py` (optional) ---------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
