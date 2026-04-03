// index.js for MCA SpamGuard Project

document.getElementById("prediction-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the default form submission

    const resultContainer = document.getElementById("result-container");
    const submitButton = document.querySelector(".predict1");
    
    // Premium Loading State
    resultContainer.innerHTML = `
        <div class="loader-container" style="display: flex; flex-direction: column; align-items: center; margin-top: 2rem;">
            <div class="spinner"></div>
            <p style="color: var(--text-muted); font-size: 0.875rem;">Analyzing patterns with Naive Bayes...</p>
        </div>
    `;
    submitButton.disabled = true;
    submitButton.style.opacity = "0.5";
    submitButton.style.cursor = "not-allowed";

    // Make an AJAX request to get the prediction result
    fetch("/predict", {
        method: "POST",
        body: new FormData(this)
    })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "Model analysis failed");
            }
            return data;
        })
        .then(data => {
            const prediction = data.prediction;
            const confidence = data.confidence;
            const badgeClass = prediction === "Spam" ? "badge-spam" : "badge-ham";
            const icon = prediction === "Spam" ? "fa-triangle-exclamation" : "fa-circle-check";
            
            // Display the result with a premium glass badge
            resultContainer.innerHTML = `
                <div class="prediction-result ${badgeClass}">
                    <span class="label" style="display: block; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.75rem;">
                        <i class="fas ${icon}"></i> AI Prediction Results
                    </span>
                    <span class="value" style="font-size: 2.5rem; font-weight: 800; display: block;">${prediction}</span>
                    <div class="confidence-meter">
                        <div class="confidence-bar" style="width: ${confidence}%"></div>
                    </div>
                    <span class="confidence-text" style="font-weight: 600; opacity: 0.8;">${confidence}% Prediction Confidence</span>
                </div>
            `;
        })
        .catch(error => {
            console.error(error);
            resultContainer.innerHTML = `
                <div style="color: #ef4444; padding: 1.5rem; border-radius: 1rem; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); margin-top: 2rem;">
                    <strong style="display: block; margin-bottom: 0.25rem;">Analysis Error:</strong> ${error.message}
                </div>
            `;
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.style.opacity = "1";
            submitButton.style.cursor = "pointer";
        });
});

// Clear button logic
document.getElementById("clear-button").addEventListener("click", function () {
    document.getElementById("message").value = "";
    document.getElementById("result-container").innerHTML = "";
    document.getElementById("message").focus();
});
