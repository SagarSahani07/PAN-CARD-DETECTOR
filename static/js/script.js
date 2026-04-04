const originalInput = document.getElementById("originalImage");
const tamperedInput = document.getElementById("tamperedImage");

const preview1 = document.getElementById("preview1");
const preview2 = document.getElementById("preview2");

const text1 = document.getElementById("text1");
const text2 = document.getElementById("text2");

function previewImage(input, previewElement, textElement) {
    const file = input.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.style.display = "block";
            textElement.style.display = "none";
        };

        reader.readAsDataURL(file);
    }
}

originalInput.addEventListener("change", function() {
    previewImage(originalInput, preview1, text1);
});

tamperedInput.addEventListener("change", function() {
    previewImage(tamperedInput, preview2, text2);
});

const dropZones = document.querySelectorAll(".drop-zone");

dropZones.forEach((zone) => {
    zone.addEventListener("dragover", (e) => {
        e.preventDefault();
        zone.style.borderColor = "#7c3aed";
        zone.style.background = "rgba(124, 58, 237, 0.12)";
    });

    zone.addEventListener("dragleave", () => {
        zone.style.borderColor = "rgba(255,255,255,0.15)";
        zone.style.background = "rgba(255,255,255,0.02)";
    });

    zone.addEventListener("drop", (e) => {
        e.preventDefault();

        zone.style.borderColor = "rgba(255,255,255,0.15)";
        zone.style.background = "rgba(255,255,255,0.02)";

        const files = e.dataTransfer.files;

        if (files.length > 0) {
            const inputId = zone.getAttribute("for");

            if (inputId === "originalImage") {
                originalInput.files = files;
                previewImage(originalInput, preview1, text1);
            } else if (inputId === "tamperedImage") {
                tamperedInput.files = files;
                previewImage(tamperedInput, preview2, text2);
            }
        }
    });
});

const analyzeButton = document.querySelector(".analyze-btn");

analyzeButton.addEventListener("click", function() {
    analyzeButton.innerHTML = "Analyzing...";
    analyzeButton.style.opacity = "0.8";
});