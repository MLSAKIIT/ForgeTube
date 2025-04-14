// ForgeTube Web UI JavaScript

// Task status polling
function pollTaskStatus(taskId) {
  const statusElement = document.getElementById("task-status");
  const progressBar = document.getElementById("progress-bar");

  if (!statusElement || !progressBar) return;

  const updateStatus = () => {
    fetch(`/api/task/${taskId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch task status");
        }
        return response.json();
      })
      .then((data) => {
        // Update status text
        statusElement.textContent = data.status;

        // Update progress bar
        let progress = 0;
        const statusMap = {
          Queued: 5,
          "Generating script...": 15,
          "Script generated": 25,
          "Generating images...": 40,
          "Generating audio...": 60,
          "Assembling video...": 80,
          Completed: 100,
          Error: 100,
        };

        progress = statusMap[data.status] || 0;
        progressBar.style.width = `${progress}%`;

        // Add appropriate classes based on status
        document.querySelectorAll(".badge").forEach((badge) => {
          badge.classList.remove(
            "badge-queued",
            "badge-processing",
            "badge-completed",
            "badge-error"
          );
        });

        const badgeElement = document.getElementById("status-badge");
        if (badgeElement) {
          if (data.status === "Completed") {
            badgeElement.classList.add("badge-completed");

            // Show the result section if available
            const resultSection = document.getElementById("result-section");
            if (resultSection) {
              resultSection.classList.remove("hidden");
            }

            // Update video source if available
            const videoElement = document.getElementById("result-video");
            if (videoElement && data.result_url) {
              videoElement.src = data.result_url;
              videoElement.load();
            }

            // No need to poll anymore
            return;
          } else if (data.status.includes("Error")) {
            badgeElement.classList.add("badge-error");
          } else if (data.status === "Queued") {
            badgeElement.classList.add("badge-queued");
          } else {
            badgeElement.classList.add("badge-processing");
          }
        }

        // Continue polling if not completed or error
        if (data.status !== "Completed" && !data.status.includes("Error")) {
          setTimeout(updateStatus, 2000);
        }
      })
      .catch((error) => {
        console.error("Error polling task status:", error);
        statusElement.textContent = "Error checking status";

        // Try again after a longer delay
        setTimeout(updateStatus, 5000);
      });
  };

  // Start polling
  updateStatus();
}

// Format JSON for display
function formatJSON(jsonObj) {
  return JSON.stringify(jsonObj, null, 2)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(
      /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
      function (match) {
        let cls = "json-number";
        if (/^"/.test(match)) {
          if (/:$/.test(match)) {
            cls = "json-key";
          } else {
            cls = "json-string";
          }
        } else if (/true|false/.test(match)) {
          cls = "json-boolean";
        } else if (/null/.test(match)) {
          cls = "json-null";
        }
        return '<span class="' + cls + '">' + match + "</span>";
      }
    );
}

// Initialize JSON viewer if present
document.addEventListener("DOMContentLoaded", function () {
  const jsonContainer = document.getElementById("json-content");
  if (jsonContainer && jsonContainer.dataset.json) {
    try {
      const jsonObj = JSON.parse(jsonContainer.dataset.json);
      jsonContainer.innerHTML = `<pre>${formatJSON(jsonObj)}</pre>`;
    } catch (e) {
      console.error("Error parsing JSON:", e);
      jsonContainer.innerHTML = `<pre>Error parsing JSON: ${e.message}</pre>`;
    }
  }

  // Initialize task polling if on task page
  const taskContainer = document.getElementById("task-container");
  if (taskContainer && taskContainer.dataset.taskId) {
    pollTaskStatus(taskContainer.dataset.taskId);
  }
});

// Form validation
document.addEventListener("DOMContentLoaded", function () {
  const createForm = document.getElementById("create-form");
  if (createForm) {
    createForm.addEventListener("submit", function (event) {
      const topic = document.getElementById("topic").value.trim();
      const geminiApi = document.getElementById("gemini_api").value.trim();
      const serpApi = document.getElementById("serp_api").value.trim();

      let isValid = true;
      let errorMessage = "";

      if (!topic) {
        isValid = false;
        errorMessage += "Topic is required. ";
      }

      if (!geminiApi) {
        isValid = false;
        errorMessage += "Gemini API key is required. ";
      }

      if (!serpApi) {
        isValid = false;
        errorMessage += "Serp API key is required. ";
      }

      if (!isValid) {
        event.preventDefault();

        const errorElement = document.getElementById("form-error");
        if (errorElement) {
          errorElement.textContent = errorMessage;
          errorElement.classList.remove("hidden");

          // Scroll to error
          errorElement.scrollIntoView({ behavior: "smooth" });
        }
      }
    });
  }
});
