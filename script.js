document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".post-form form");

    if (form) {
        form.addEventListener("submit", function () {
            const button = form.querySelector("button");

            if (button) {
                button.textContent = "Publishing...";
                button.disabled = true;
            }
        });
    }
});