/*--------------------------- Get Date --------------------------- */

const getYear = () => {
  const today = new Date();
  return today.getFullYear();
};

document.querySelector(".year").textContent = getYear();

if (document.getElementById("logoutBtn")) {
  document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("full_name");

    setTimeout(() => {
      window.location.assign("http://127.0.0.1:3000/public/index.html");
    }, 500);
  });
}
