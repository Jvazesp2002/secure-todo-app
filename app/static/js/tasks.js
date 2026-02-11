document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".toggle-btn");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const taskId = button.dataset.taskId;
            const desc = document.getElementById(`desc-${taskId}`);

            if (desc.classList.contains("hidden")) {
                desc.classList.remove("hidden");
                button.textContent = "Ocultar descripción";
                button.classList.replace("bg-indigo-50", "bg-gray-200");
            } else {
                desc.classList.add("hidden");
                button.textContent = "Ver descripción";
                button.classList.replace("bg-gray-200", "bg-indigo-50");
            }
        });
    });
});