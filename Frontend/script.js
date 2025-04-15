const form = document.getElementById('uploadForm');
const imageInput = document.getElementById('imageInput');
const statusDiv = document.getElementById('status');
const resultCard = document.getElementById('resultCard');
const verdictEl = document.getElementById('verdict');
const reasonEl = document.getElementById('reason');
const historySection = document.getElementById('historySection');
const historyList = document.getElementById('historyList');

let history = [];
const API_ENDPOINT = "http://127.0.0.1:5000/analyze";

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const file = imageInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('image', file);

  statusDiv.classList.remove('hidden');
  statusDiv.textContent = '🔄 Analyzing...';
  resultCard.classList.add('hidden');

  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    const data = await response.json();
    verdictEl.textContent = `📌 Verdict: ${data.result}`;
    reasonEl.textContent = `🧠 Reason: ${data.reason}`;

    resultCard.classList.remove('hidden');
    statusDiv.classList.add('hidden');

    history.unshift({
      verdict: data.result,
      reason: data.reason,
      time: new Date().toLocaleString()
    });

    updateHistoryUI();
  } catch (err) {
    console.error("[Frontend] Error:", err);
    statusDiv.textContent = "❌ Error analyzing image. Check server.";
  }
});

function updateHistoryUI() {
  historySection.classList.remove('hidden');
  historyList.innerHTML = '';
  history.slice(0, 5).forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${item.verdict}</strong><br /><em>${item.reason}</em><br /><small>${item.time}</small>`;
    historyList.appendChild(li);
  });
}
