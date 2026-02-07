document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".toggle-btn");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const taskId = button.dataset.taskId;
            const desc = document.getElementById(`desc-${taskId}`);

            if (desc.style.display === "none") {
                desc.style.display = "block";
                button.textContent = "Ocultar descripción";
            } else {
                desc.style.display = "none";
                button.textContent = "Ver descripción";
            }
        });
    });
});
