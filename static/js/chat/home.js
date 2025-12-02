
    // Auto-hide error after 3 seconds
    document.addEventListener("DOMContentLoaded", function() {
        const errorBox = document.querySelector(".error-text");
        if (errorBox) {
            setTimeout(() => {
                errorBox.style.transition = "opacity 0.5s ease";
                errorBox.style.opacity = "0";

                // Remove from DOM after fade-out
                setTimeout(() => errorBox.remove(), 500);
            }, 3000);
        }
    });