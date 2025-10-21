document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("lesson-container");
  const contextMenu = document.getElementById("context-menu");
  const sidePanel = document.getElementById("side-panel");
  const panelContent = document.getElementById("panel-content");

  let contextX = 0;
  let contextY = 0;

  // 🔹 Load lesson file dynamically (?file=filename.md)
  const params = new URLSearchParams(window.location.search);
  const file = params.get("file");
  if (file) {
    fetch(`/markdown/${file}`)
      .then(res => res.text())
      .then(data => {
        container.innerHTML = marked.parse(data); // ✅ Convert Markdown to HTML
      })
      .catch(err => {
        container.innerText = "Error loading file: " + err.message;
      });
  }

  // 🔹 Right-click context menu
  container.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    contextX = e.pageX;
    contextY = e.pageY;
    contextMenu.style.top = `${e.pageY}px`;
    contextMenu.style.left = `${e.pageX}px`;
    contextMenu.style.display = "block";
  });

  // Hide menu when clicking outside
  document.addEventListener("click", () => {
    contextMenu.style.display = "none";
  });

  // 🔹 Insert Image
  document.getElementById("insert-image").addEventListener("click", () => {
    openPanel(
      "Insert Image",
      `
      <input type="text" id="image-search" placeholder="Search images..." style="width:100%; margin-bottom:10px;">
      <button onclick="searchImage()">Search</button>
      <div id="image-results"></div>
    `
    );
    contextMenu.style.display = "none";
  });

  // 🔹 Insert Audio
  document.getElementById("insert-audio").addEventListener("click", () => {
    openPanel(
      "Insert Audio",
      `
      <textarea id="audio-text" rows="3" style="width:100%; margin-bottom:10px;" placeholder="Enter text for audio..."></textarea>
      <button onclick="generateAudio()">Generate Audio</button>
    `
    );
    contextMenu.style.display = "none";
  });

  // 🔹 Side Panel Functions
  document.getElementById("close-panel").addEventListener("click", () => {
    sidePanel.style.right = "-400px";
  });

  window.openPanel = function (title, html) {
    document.getElementById("panel-title").textContent = title;
    panelContent.innerHTML = html;
    sidePanel.style.right = "0px";
  };

  // 🔹 Search Image Function
  window.searchImage = function () {
    const q = document.getElementById("image-search").value.trim();
    if (!q) return;
    const resultsDiv = document.getElementById("image-results");
    resultsDiv.innerHTML = "<p>Searching...</p>";

    fetch(`/api/search_images?q=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(images => {
        resultsDiv.innerHTML = "";
        if (!Array.isArray(images)) {
          resultsDiv.innerHTML = "<p>No images found.</p>";
          return;
        }
        images.forEach(url => {
          const img = document.createElement("img");
          img.src = url;
          img.onclick = () => {
            insertAtCursor(`<img src="${url}" alt="Lesson Image">`);
            sidePanel.style.right = "-400px";
          };
          resultsDiv.appendChild(img);
        });
      })
      .catch(() => {
        resultsDiv.innerHTML = "<p style='color:red;'>Error fetching images</p>";
      });
  };

  // 🔹 Generate Audio Function
  window.generateAudio = function () {
    const text = document.getElementById("audio-text").value.trim();
    if (!text) return;

    fetch("/api/generate_audio", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text })
    })
      .then(res => res.json())
      .then(data => {
        const audioHTML = `<audio controls><source src="${data.audio_url}" type="audio/mpeg"></audio>`;
        insertAtCursor(audioHTML);
        sidePanel.style.right = "-400px";
      })
      .catch(() => {
        alert("Error generating audio.");
      });
  };

  // 🔹 Helper: Insert HTML at the clicked position
  function insertAtCursor(html) {
    const range = document.caretRangeFromPoint(contextX, contextY);
    if (!range) return;
    const frag = range.createContextualFragment(html);
    range.insertNode(frag);
  }

  // 🔹 Double-click image to edit or replace
  container.addEventListener("dblclick", (e) => {
    if (e.target.tagName === "IMG") {
      const currentImg = e.target;
      const currentAlt = currentImg.alt || "";
      const currentSrc = currentImg.src;

      const newAlt = prompt("Edit alt text:", currentAlt);
      if (newAlt === null) return;
      currentImg.alt = newAlt;

      const replace = confirm("Do you want to replace this image?");
      if (replace) {
        const newUrl = prompt("Enter new image URL:", currentSrc);
        if (newUrl && newUrl !== currentSrc) {
          currentImg.src = newUrl;
        }
      }
    }
  });

  // 🔹 Double-click audio to replace source
  container.addEventListener("dblclick", (e) => {
    if (e.target.tagName === "AUDIO" || e.target.closest("audio")) {
      const audioElem = e.target.tagName === "AUDIO" ? e.target : e.target.closest("audio");
      const sourceElem = audioElem.querySelector("source");
      const currentSrc = sourceElem?.src || "";

      const newSrc = prompt("Enter new audio file URL:", currentSrc);
      if (newSrc && newSrc !== currentSrc) {
        sourceElem.src = newSrc;
        audioElem.load(); // Reload audio
      }
    }
  });
});