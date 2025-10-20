document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("lesson-container");
  const contextMenu = document.getElementById("context-menu");
  const sidePanel = document.getElementById("side-panel");
  const panelContent = document.getElementById("panel-content");

  let contextX = 0;
  let contextY = 0;

  // Load lesson file from ?file=...
  const params = new URLSearchParams(window.location.search);
  const file = params.get("file");
  if (file) {
    fetch(`/markdown/${file}`)
      .then(res => res.text())
      .then(data => {
        container.innerText = data;
      });
  }

  // Show context menu
  container.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    contextX = e.pageX;
    contextY = e.pageY;
    contextMenu.style.top = `${e.pageY}px`;
    contextMenu.style.left = `${e.pageX}px`;
    contextMenu.style.display = "block";
  });

  // Insert Image
  document.getElementById("insert-image").addEventListener("click", () => {
    openPanel("Insert Image", `<input type="text" id="image-search" placeholder="Search...">
      <button onclick="searchImage()">Search</button>
      <div id="image-results"></div>`);
    contextMenu.style.display = "none";
  });

  // Insert Audio
  document.getElementById("insert-audio").addEventListener("click", () => {
    openPanel("Insert Audio", `<input type="text" id="audio-text" placeholder="Enter text for audio">
      <button onclick="generateAudio()">Generate</button>`);
    contextMenu.style.display = "none";
  });

  // Close side panel
  document.getElementById("close-panel").addEventListener("click", () => {
    sidePanel.style.display = "none";
  });

  window.openPanel = function(title, html) {
    document.getElementById("panel-title").textContent = title;
    panelContent.innerHTML = html;
    sidePanel.style.display = "flex";
  };

  window.searchImage = function() {
    const q = document.getElementById("image-search").value;
    fetch(`/api/search_images?q=${q}`)
      .then(res => res.json())
      .then(images => {
        const div = document.getElementById("image-results");
        div.innerHTML = "";
        images.forEach(url => {
          const img = document.createElement("img");
          img.src = url;
          img.style.width = "100%";
          img.style.margin = "5px 0";
          img.onclick = () => {
            insertAtPosition(`<img src="${url}" alt="Image"/>`);
            sidePanel.style.display = "none";
          };
          div.appendChild(img);
        });
      });
  };

  window.generateAudio = function() {
    const text = document.getElementById("audio-text").value;
    fetch("/api/generate_audio", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text })
    })
    .then(res => res.json())
    .then(data => {
      const audioHTML = `<audio controls><source src="${data.audio_url}" type="audio/mpeg"></audio>`;
      insertAtPosition(audioHTML);
      sidePanel.style.display = "none";
    });
  };

  function insertAtPosition(html) {
    const range = document.caretRangeFromPoint(contextX, contextY);
    if (range) {
      const frag = range.createContextualFragment(html);
      range.insertNode(frag);
    }
  }

  // Hide context menu on click elsewhere
  document.addEventListener("click", () => {
    contextMenu.style.display = "none";
  });
});