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

const canvas = document.getElementById('iconCloudCanvas');
const ctx = canvas.getContext('2d');

const icons = [
  "assets/css.png",
  "assets/exiftool.png",
  "assets/flask.png",
  "assets/github.png",
  "assets/html.png",
  "assets/js.png",
  "assets/python.png",
  "assets/sightengine.png",
  "assets/sqlite.png",
  "assets/magicui.png"
];

const iconSize = 65;
const radius = 120;
let mouse = { x: canvas.width / 2, y: canvas.height / 2 };
let rotation = { x: 0, y: 0 };
let targetRotation = { x: 0, y: 0 };
let images = [];

icons.forEach((src, i) => {
  const img = new Image();
  img.src = src;
  img.onload = () => {
    images[i] = img;
  };
});

const centerX = canvas.width / 2;
const centerY = canvas.height / 2;

// Fibonacci sphere distribution
function generateSpherePoints(numPoints) {
  const points = [];
  const offset = 2 / numPoints;
  const increment = Math.PI * (3 - Math.sqrt(5));

  for (let i = 0; i < numPoints; i++) {
    const y = i * offset - 1 + offset / 2;
    const r = Math.sqrt(1 - y * y);
    const phi = i * increment;
    const x = Math.cos(phi) * r;
    const z = Math.sin(phi) * r;
    points.push({ x: x * 100, y: y * 100, z: z * 100 });
  }

  return points;
}

const icons3D = generateSpherePoints(icons.length);

canvas.addEventListener("mousemove", (e) => {
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
});

function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3);
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const dx = mouse.x - centerX;
  const dy = mouse.y - centerY;
  const maxDistance = Math.sqrt(centerX ** 2 + centerY ** 2);
  const distance = Math.sqrt(dx ** 2 + dy ** 2);
  const speed = 0.003 + (distance / maxDistance) * 0.01;

  rotation.x += (dy / canvas.height) * speed;
  rotation.y += (dx / canvas.width) * speed;

  icons3D.forEach((icon, i) => {
    const cosX = Math.cos(rotation.x);
    const sinX = Math.sin(rotation.x);
    const cosY = Math.cos(rotation.y);
    const sinY = Math.sin(rotation.y);

    const x1 = icon.x * cosY - icon.z * sinY;
    const z1 = icon.x * sinY + icon.z * cosY;
    const y1 = icon.y * cosX - z1 * sinX;
    const z2 = icon.y * sinX + z1 * cosX;

    const scale = (z2 + 200) / 300;
    const opacity = Math.max(0.2, Math.min(1, (z2 + 150) / 200));

    ctx.save();
    ctx.translate(centerX + x1, centerY + y1);
    ctx.scale(scale, scale);
    ctx.globalAlpha = opacity;

    if (images[i]) {
      const img = images[i];
      const aspectRatio = img.width / img.height;
          
      let drawWidth, drawHeight;
      if (aspectRatio >= 1) {
        drawWidth = iconSize;
        drawHeight = iconSize / aspectRatio;
      } else {
        drawHeight = iconSize;
        drawWidth = iconSize * aspectRatio;
      }
      
      ctx.drawImage(img, -drawWidth / 2, -drawHeight / 2, drawWidth, drawHeight);
      
    }

    ctx.restore();
  });

  requestAnimationFrame(animate);
}

animate();

function scrollToSection(id) {
  const section = document.getElementById(id);
  if (section) section.scrollIntoView({ behavior: "smooth" });
}

function copyEmail(email) {
  navigator.clipboard.writeText(email).then(() => {
    alert("Email copied to clipboard!");
  });
}

function toggleTheme() {
  document.body.classList.toggle("dark-mode");

}
