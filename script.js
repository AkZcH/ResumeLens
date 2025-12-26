// ================= CONFIGURATION =================
const API_URL = "http://127.0.0.1:8000";

// ================= GLOBAL STATE =================
let analysisData = null;

// ================= LANDING → DASHBOARD =================
function goToDashboard() {
  document.getElementById("landing").style.display = "none";
  document.getElementById("dashboards").style.display = "block";
  updateProgressBar(1);
}

function updateProgressBar(step) {
  document.querySelectorAll(".step").forEach((el, index) => {
    el.classList.toggle("active", index + 1 <= step);
  });
}

// ================= PARTICLES =================
function createParticles() {
  const container = document.getElementById("particles-bg");
  if (!container) return;

  for (let i = 0; i < 80; i++) {
    const p = document.createElement("div");
    p.className = "particle";
    p.style.left = `${Math.random() * 100}%`;
    p.style.top = `${Math.random() * 100}%`;
    container.appendChild(p);
  }
}
window.addEventListener("load", createParticles);

// ================= FILE UPLOAD UI =================
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("resume-file");
  const uploadZone = document.getElementById("upload-zone");
  const fileName = document.getElementById("file-name");

  fileInput.addEventListener("change", e => {
    if (e.target.files[0]) {
      fileName.textContent = `✅ ${e.target.files[0].name}`;
      fileName.style.color = "#90ee90";
    }
  });

  uploadZone.addEventListener("dragover", e => {
    e.preventDefault();
    uploadZone.style.borderColor = "#8a2be2";
  });

  uploadZone.addEventListener("dragleave", () => {
    uploadZone.style.borderColor = "#444";
  });

  uploadZone.addEventListener("drop", e => {
    e.preventDefault();
    uploadZone.style.borderColor = "#444";

    if (e.dataTransfer.files[0]) {
      fileInput.files = e.dataTransfer.files;
      fileName.textContent = `✅ ${e.dataTransfer.files[0].name}`;
      fileName.style.color = "#90ee90";
    }
  });
});

// ================= MAIN ANALYSIS =================
async function analyzeResume() {
  const fileInput = document.getElementById("resume-file");
  const jdInput = document.getElementById("job-description");

  const file = fileInput.files[0];
  if (!file) {
    alert("Please upload a resume");
    return;
  }

  document.getElementById("analyze-text").style.display = "none";
  document.getElementById("analyze-loader").style.display = "inline";

  const formData = new FormData();
  formData.append("resume", file);

  if (jdInput.value.trim()) {
    formData.append("job_description", jdInput.value.trim());
  }

  try {
    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      body: formData
    });

    analysisData = await res.json();
    populateDashboard(analysisData);

  } catch (err) {
    console.error(err);
    alert("Analysis failed");
  } finally {
    document.getElementById("analyze-text").style.display = "inline";
    document.getElementById("analyze-loader").style.display = "none";
  }
}

// ================= DASHBOARD 2 =================
function populateDashboard(data) {
  document.getElementById("dashboard-1").style.display = "none";
  document.getElementById("dashboard-2").style.display = "block";
  updateProgressBar(2);

  document.getElementById("ats-score").innerText = data.ats_score;
  document.getElementById("keyword-score").innerText = data.keyword_match;
  document.getElementById("skill-score").innerText = data.skill_match;
  document.getElementById("missing-count").innerText = data.missing_skills.length;

  const matched = document.getElementById("matched-skills");
  const missing = document.getElementById("missing-skills");
  const suggestions = document.getElementById("suggestions-list");

  matched.innerHTML = "";
  missing.innerHTML = "";
  suggestions.innerHTML = "";

  data.matched_skills.forEach(s =>
    matched.innerHTML += `<span class="tag">${s}</span>`
  );

  data.missing_skills.forEach(s =>
    missing.innerHTML += `<span class="tag missing">${s}</span>`
  );

  data.suggestions.forEach(s =>
    suggestions.innerHTML += `<li>${s}</li>`
  );

  renderImprovements(data.improved_bullets);
}

// ================= DASHBOARD 3 =================
function goToImprovements() {
  document.getElementById("dashboard-2").style.display = "none";
  document.getElementById("dashboard-3").style.display = "block";
  updateProgressBar(3);
}

function renderImprovements(bullets) {
  const container = document.getElementById("bullet-improvements");
  container.innerHTML = "";

  bullets.forEach(b =>
    container.innerHTML += `<div class="improved-bullet">${b}</div>`
  );
}

// ================= RESET =================
function resetDashboard() {
  location.reload();
}
