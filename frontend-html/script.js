// ================= GLOBAL VARIABLES =================
let resumeFile = null;
let analysisData = null;



// ================= PARTICLE ANIMATION =================
function createParticles() {
  const particlesContainer = document.getElementById('particles-bg');
  
  for (let i = 0; i < 100; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.cssText = `
      position: absolute;
      width: ${Math.random() * 4 + 2}px;
      height: ${Math.random() * 4 + 2}px;
      background: rgba(138, 43, 226, ${Math.random() * 0.5 + 0.2});
      border-radius: 50%;
      left: ${Math.random() * 100}%;
      top: ${Math.random() * 100}%;
      animation: float ${Math.random() * 10 + 15}s linear infinite;
      box-shadow: 0 0 10px rgba(138, 43, 226, 0.5);
    `;
    particlesContainer.appendChild(particle);
  }
}

// CSS animation for particles
const style = document.createElement('style');
style.textContent = `
  @keyframes float {
    0% { transform: translateY(0) translateX(0); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(-100vh) translateX(${Math.random() * 100 - 50}px); opacity: 0; }
  }
`;
document.head.appendChild(style);

// Initialize particles on load
window.addEventListener('load', createParticles);





// ================= NAVIGATION FUNCTIONS =================
function goToDashboard() {
  document.getElementById("landing").style.display = "none";
  document.getElementById("dashboards").style.display = "block";
  updateProgressBar(1);
}

function updateProgressBar(step) {
  const steps = document.querySelectorAll(".step");
  steps.forEach((stepEl, index) => {
    stepEl.classList.toggle("active", index + 1 <= step);
  });
}

// ================= FILE UPLOAD HANDLING =================
document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("resume-file");
  const uploadZone = document.getElementById("upload-zone");
  const fileName = document.getElementById("file-name");

  fileInput.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
      resumeFile = file;
      fileName.textContent = `✅ ${file.name}`;
      fileName.style.color = "#90ee90";
    }
  });

  uploadZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    uploadZone.style.borderColor = "#8a2be2";
    uploadZone.style.background = "rgba(138, 43, 226, 0.1)";
  });

  uploadZone.addEventListener("dragleave", function (e) {
    e.preventDefault();
    uploadZone.style.borderColor = "#444";
    uploadZone.style.background = "transparent";
  });

  uploadZone.addEventListener("drop", function (e) {
    e.preventDefault();
    uploadZone.style.borderColor = "#444";
    uploadZone.style.background = "transparent";

    const file = e.dataTransfer.files[0];
    if (file) {
      resumeFile = file;
      fileName.textContent = `✅ ${file.name}`;
      fileName.style.color = "#90ee90";
    }
  });
});

// ================= ANALYZE RESUME =================
function analyzeResume() {
  const jobDescription = document.getElementById("job-description").value;

  if (!resumeFile) {
    alert("⚠️ Please upload your resume first!");
    return;
  }

  if (!jobDescription.trim()) {
    alert("⚠️ Please paste the job description!");
    return;
  }

  const analyzeText = document.getElementById("analyze-text");
  const analyzeLoader = document.getElementById("analyze-loader");
  analyzeText.style.display = "none";
  analyzeLoader.style.display = "inline";

  setTimeout(() => {
    analysisData = {
      ats_score: 78.5,
      keyword_match: 65.2,
      skill_match: 82.0,
      semantic_similarity: 71.3,
      matched_skills: [
        "Python",
        "SQL",
        "Machine Learning",
        "Git",
        "REST API",
        "FastAPI",
      ],
      missing_skills: ["Docker", "Kubernetes", "AWS", "React"],
      suggestions: [
        "✅ Good match! Minor improvements needed.",
        "Add these skills: Docker, Kubernetes, AWS, React",
        "Use action verbs like 'Developed', 'Led', 'Achieved'",
        "Quantify achievements with numbers and metrics",
        "Highlight leadership and impact in projects",
      ],
      resume_bullets: [
        "Worked on ML models",
        "Built data pipelines",
        "Created dashboards",
      ],
      improved_bullets: [
        "Developed supervised ML models using Python and TensorFlow, improving prediction accuracy by 23%",
        "Built scalable data pipelines processing 500K+ records daily using SQL",
        "Created dashboards reducing reporting time by 40%",
      ],
    };

    analyzeText.style.display = "inline";
    analyzeLoader.style.display = "none";

    displayAnalysisResults();

    document.getElementById("dashboard-1").style.display = "none";
    document.getElementById("dashboard-2").style.display = "block";
    updateProgressBar(2);

    window.scrollTo({ top: 0, behavior: "smooth" });
  }, 2000);
}

// ================= DISPLAY ANALYSIS RESULTS =================
function displayAnalysisResults() {
  document.getElementById(
    "ats-score"
  ).textContent = `${analysisData.ats_score}%`;
  document.getElementById(
    "keyword-score"
  ).textContent = `${analysisData.keyword_match}%`;
  document.getElementById(
    "skill-score"
  ).textContent = `${analysisData.skill_match}%`;
  document.getElementById("missing-count").textContent =
    analysisData.missing_skills.length;

  const matchedSkills = document.getElementById("matched-skills");
  matchedSkills.innerHTML = "";
  analysisData.matched_skills.forEach((skill) => {
    const tag = document.createElement("span");
    tag.className = "tag green";
    tag.textContent = skill;
    matchedSkills.appendChild(tag);
  });

  const missingSkills = document.getElementById("missing-skills");
  missingSkills.innerHTML = "";
  analysisData.missing_skills.forEach((skill) => {
    const tag = document.createElement("span");
    tag.className = "tag red";
    tag.textContent = skill;
    missingSkills.appendChild(tag);
  });

  const suggestionsList = document.getElementById("suggestions-list");
  suggestionsList.innerHTML = "";
  analysisData.suggestions.forEach((text) => {
    const li = document.createElement("li");
    li.textContent = text;
    suggestionsList.appendChild(li);
  });
}

// ================= IMPROVEMENTS =================
function goToImprovements() {
  document.getElementById("dashboard-2").style.display = "none";
  document.getElementById("dashboard-3").style.display = "block";
  updateProgressBar(3);
  displayImprovements();
}

function displayImprovements() {
  const container = document.getElementById("bullet-improvements");
  container.innerHTML = "";

  analysisData.resume_bullets.forEach((bullet, i) => {
    const div = document.createElement("div");
    div.className = "bullet-compare";
    div.innerHTML = `
      <div class="bullet-card before">
        <h4>❌ Before</h4>
        <p>${bullet}</p>
      </div>
      <div class="bullet-card after">
        <h4>✅ After</h4>
        <p>${analysisData.improved_bullets[i]}</p>
        <button onclick="copyToClipboard('${analysisData.improved_bullets[
          i
        ].replace(/'/g, "\\'")}')">
          📋 Copy
        </button>
      </div>`;
    container.appendChild(div);
  });
}

// ================= UTILITIES =================
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(
    () => alert("✅ Copied to clipboard!"),
    () => alert("❌ Copy failed")
  );
}

function resetDashboard() {
  resumeFile = null;
  analysisData = null;

  document.getElementById("resume-file").value = "";
  document.getElementById("file-name").textContent =
    "Drag & drop or click to upload";
  document.getElementById("file-name").style.color = "#999";
  document.getElementById("job-description").value = "";

  document.getElementById("dashboard-3").style.display = "none";
  document.getElementById("dashboard-1").style.display = "block";
  updateProgressBar(1);
}
