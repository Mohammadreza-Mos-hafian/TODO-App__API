const togglePasswordType = (input, icon) => {
    const type = input.getAttribute("type") === "password" ? "text" : "password";
    input.setAttribute("type", type);
    icon.setAttribute("src", type === "text"
        ? "public/icons/eye_invisible.png"
        : "public/icons/eye_visible.png"
    );
}

document.querySelectorAll(".toggle-password").forEach(icon => {
    icon.addEventListener("click", () => {
        const inputId = icon.getAttribute("data-icon");
        const input = document.getElementById(inputId);
        togglePasswordType(input, icon);
    });
});