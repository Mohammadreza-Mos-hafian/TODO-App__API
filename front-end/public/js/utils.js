const togglePasswordType = (input, icon) => {
  const type = input.getAttribute("type") === "password" ? "text" : "password";
  input.setAttribute("type", type);
  icon.setAttribute(
    "src",
    type === "text"
      ? "http://127.0.0.1:3000/public/images/icons/eye_invisible.png"
      : "http://127.0.0.1:3000/public/images/icons/eye_visible.png"
  );
};

document.querySelectorAll(".toggle-password").forEach((icon) => {
  icon.addEventListener("click", () => {
    const inputType = icon.getAttribute("data-icon");
    const input = document.getElementById(inputType);
    togglePasswordType(input, icon);
  });
});
