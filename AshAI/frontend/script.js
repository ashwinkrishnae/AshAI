let questions = [];
let current = 0;
let score = 0;
let answered = false;


const startBtn = document.getElementById("start-btn");
const quizContainer = document.getElementById("quiz-container");
const questionArea = document.getElementById("question-area");
const resultArea = document.getElementById("result-area");
const nextBtn = document.getElementById("next-btn");
const restartBtn = document.getElementById("restart-btn");
const progressBar = document.getElementById("progress");
const questionCount = document.getElementById("question-count");
const themeToggle = document.getElementById("theme-toggle");
const quantBtn = document.getElementById("quant-btn");
const compBtn = document.getElementById("comp-btn");
const engBtn = document.getElementById("eng-btn");
const mathBtn = document.getElementById("math-btn");
const reasonBtn = document.getElementById("reason-btn");
const stopBtn = document.getElementById("stop-btn");

// Theme toggle logic
themeToggle.onclick = function() {
  document.body.classList.toggle("dark-mode");
  // Change icon
  if (document.body.classList.contains("dark-mode")) {
    themeToggle.innerText = "☀️";
    themeToggle.title = "Switch to light mode";
  } else {
    themeToggle.innerText = "🌙";
    themeToggle.title = "Switch to dark mode";
  }
  localStorage.setItem("ssc-theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
};

// On load, set theme from localStorage
window.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("ssc-theme");
  if (saved === "dark") {
    document.body.classList.add("dark-mode");
    themeToggle.innerText = "☀️";
    themeToggle.title = "Switch to light mode";
  } else {
    themeToggle.innerText = "🌙";
    themeToggle.title = "Switch to dark mode";
  }
});



startBtn.onclick = () => startQuiz("general");
quantBtn.onclick = () => startQuiz("quant");
compBtn.onclick = () => startQuiz("computer");
engBtn.onclick = () => startQuiz("english");
mathBtn.onclick = () => startQuiz("mathematics");
reasonBtn.onclick = () => startQuiz("reasoning");
restartBtn.onclick = () => startQuiz(lastQuizType);
nextBtn.onclick = nextQuestion;
stopBtn.onclick = stopQuiz;

let lastQuizType = "general";



function startQuiz(type = "general") {
  lastQuizType = type;
  document.getElementById("quiz-select-row").style.display = "none";
  quizContainer.style.display = "block";
  restartBtn.style.display = "none";
  resultArea.innerHTML = "";
  score = 0;
  current = 0;
  answered = false;
  updateProgress();
  fetchQuestions(type);
  stopBtn.style.display = "inline-block";
}



function fetchQuestions(type) {
  let url = "http://127.0.0.1:8000/fetch_external_questions";
  if (type === "quant") {
    url = "http://127.0.0.1:8000/fetch_quant_questions";
  } else if (type === "computer") {
    url = "http://127.0.0.1:8000/fetch_computer_questions";
  } else if (type === "english") {
    url = "http://127.0.0.1:8000/fetch_english_questions";
  } else if (type === "mathematics") {
    url = "http://127.0.0.1:8000/fetch_mathematics_questions";
  } else if (type === "reasoning") {
    url = "http://127.0.0.1:8000/fetch_reasoning_questions";
  }
  fetch(url)
    .then(res => res.json())
    .then(data => {
      questions = data;
      showQuestion();
    });
}

function showQuestion() {
  if (current >= questions.length) {
    showSummary();
    return;
  }
  answered = false;
  updateProgress();
  const q = questions[current];
  let meta = '';
  if (q.category || q.source) {
    meta = `<div style="font-size:13px;color:#888;margin-bottom:4px;">
      ${q.category ? `<span style='margin-right:10px;'>Category: <b>${q.category}</b></span>` : ''}
      ${q.source ? `<span>Source: <b>${q.source}</b></span>` : ''}
    </div>`;
  }
  questionArea.innerHTML = `
    <div class="question-card">
      ${meta}
      <div style="font-size:16px;margin-bottom:8px;"><strong>Q${current + 1}.</strong> ${q.question}</div>
      <div id="options-area">
        ${q.options.map(opt => `
          <button class="option-btn" style="margin:4px 0;width:100%;text-align:left;">${opt}</button>
        `).join("")}
      </div>
    </div>
  `;
  resultArea.innerHTML = "";
  nextBtn.style.display = "none";
  // Attach event listeners immediately after updating innerHTML
  const optionButtons = document.querySelectorAll('.option-btn');
  optionButtons.forEach(btn => {
    btn.onclick = () => submitAnswer(q, btn.innerText, btn);
  });
}

function submitAnswer(q, answer, btn) {
  if (answered) return;
  answered = true;
  // If the question has no id or is from external source, check answer on frontend
  if (typeof q.id === 'undefined' || !q.explanation) {
    const isCorrect = answer === q.answer;
    if (isCorrect) score++;
    resultArea.innerHTML = `
      <p><strong>${isCorrect ? "✅ Correct!" : "❌ Wrong!"}</strong></p>
      <p>Correct Answer: ${q.answer}</p>
    `;
    document.querySelectorAll('.option-btn').forEach(b => {
      b.disabled = true;
      if (b.innerText === q.answer) {
        b.style.background = '#c8e6c9';
        b.style.borderColor = '#388e3c';
      } else if (b.innerText === answer) {
        b.style.background = '#ffcdd2';
        b.style.borderColor = '#d32f2f';
      } else {
        b.style.opacity = 0.7;
      }
    });
    nextBtn.style.display = "inline-block";
    if (current === questions.length - 1) {
      nextBtn.innerText = "Finish";
    } else {
      nextBtn.innerText = "Next";
    }
    return;
  }
  // Otherwise, use backend validation
  fetch(`http://127.0.0.1:8000/submit?qid=${q.id}&user_answer=${encodeURIComponent(answer)}`, {
    method: "POST"
  })
    .then(res => res.json())
    .then(data => {
      if (data.correct) score++;
      resultArea.innerHTML = `
        <div style="margin-bottom:8px;"><strong>${data.correct ? "✅ Correct!" : "❌ Wrong!"}</strong></div>
        <div style="margin-bottom:8px;"><span style="font-weight:600;">Explanation:</span><br><span style="display:inline-block;padding:8px 12px;background:rgba(76,175,80,0.07);border-radius:8px;">${formatExplanation(data.explanation)}</span></div>
        <div style="margin-bottom:4px;"><span style="font-weight:600;">Difficulty:</span> <span style="padding:2px 8px;border-radius:6px;background:#e3f0ff;color:#1976d2;font-weight:500;">${data.difficulty}</span></div>
      `;
// Format explanation for better readability (add line breaks, highlight code, etc.)
function formatExplanation(expl) {
  if (!expl) return "";
  // Replace newlines with <br>, highlight code blocks (simple)
  let html = expl
    .replace(/\n/g, '<br>')
    .replace(/`([^`]+)`/g, '<code style="background:#f4f4f4;padding:2px 5px;border-radius:4px;">$1</code>');
  // If in dark mode, adjust code bg
  if (document.body.classList.contains("dark-mode")) {
    html = html.replace(/background:#f4f4f4/g, 'background:#232b3a;color:#e0e6f0');
  }
  return html;
}
      document.querySelectorAll('.option-btn').forEach(b => {
        b.disabled = true;
        if (b.innerText === q.answer) {
          b.style.background = '#c8e6c9';
          b.style.borderColor = '#388e3c';
        } else if (b.innerText === answer) {
          b.style.background = '#ffcdd2';
          b.style.borderColor = '#d32f2f';
        } else {
          b.style.opacity = 0.7;
        }
      });
      nextBtn.style.display = "inline-block";
      if (current === questions.length - 1) {
        nextBtn.innerText = "Finish";
      } else {
        nextBtn.innerText = "Next";
      }
    });
}

function nextQuestion() {
  current++;
  showQuestion();
}


function showSummary() {
  updateProgress();
  questionArea.innerHTML = "";
  // Show a summary of categories and sources if available
  let catSet = new Set();
  let srcSet = new Set();
  questions.forEach(q => {
    if (q.category) catSet.add(q.category);
    if (q.source) srcSet.add(q.source);
  });
  let meta = '';
  if (catSet.size || srcSet.size) {
    meta = `<div style='font-size:13px;color:#888;margin-bottom:8px;'>`;
    if (catSet.size) meta += `Categories: <b>${[...catSet].join(", ")}</b> `;
    if (srcSet.size) meta += `| Sources: <b>${[...srcSet].join(", ")}</b>`;
    meta += `</div>`;
  }
  resultArea.innerHTML = `<div class="question-card"><h2>Quiz Complete!</h2>${meta}<p>Your Score: ${score} / ${questions.length}</p></div>`;
  nextBtn.style.display = "none";
  restartBtn.style.display = "inline-block";
  document.getElementById("quiz-select-row").style.display = "flex";
  stopBtn.style.display = "none";
}

function stopQuiz() {
  // End the quiz early and show the summary
  showSummary();
}

function updateProgress() {
  if (!progressBar || !questionCount) return;
  let percent = questions.length ? ((current) / questions.length) * 100 : 0;
  progressBar.style.width = percent + "%";
  if (questions.length) {
    questionCount.innerText = `Question ${Math.min(current+1, questions.length)} of ${questions.length}`;
  } else {
    questionCount.innerText = "";
  }
}
