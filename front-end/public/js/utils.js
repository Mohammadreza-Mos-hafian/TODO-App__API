/*--------------------------- Toggle Icon --------------------------- */

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

export const toggleEyeIcon = () => {
  document.querySelectorAll(".toggle-password").forEach((icon) => {
    icon.addEventListener("click", () => {
      const inputType = icon.getAttribute("data-icon");
      const input = document.getElementById(inputType);
      togglePasswordType(input, icon);
    });
  });
};

/*--------------------------- Error Messages --------------------------- */

export const showErrorMessages = (errors = {}) => {
  for (let [key, value] of Object.entries(errors)) {
    if (value[0] !== "") {
      let inputParentElem = document.getElementById(`${key}`).parentElement;
      let spanElem = inputParentElem.nextElementSibling;

      if (spanElem && spanElem.classList.contains("error-message")) {
        spanElem.textContent = value[0];
        spanElem.classList.add("text-danger");
      }
    }
  }
};

export const refreshErrors = () => {
  document.querySelectorAll(".error-message").forEach((elem) => {
    elem.textContent = "";
    elem.classList.remove("text-danger");
  });
};

/*--------------------------- Redirect if Authenticated --------------------------- */

export const isAuthenticated = () => {
  document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("access_token")) {
      setTimeout(() => {
        window.location.assign(
          "http://127.0.0.1:3000/public/pages/dashboard.html"
        );
      }, 500);
    }
  });
};

/*--------------------------- Check Access Token --------------------------- */

export const apiRequest = async (url, options = {}) => {
  try {
    let response = await fetch(url, {
      ...options,
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        ...options.headers,
      },
    });

    if (response.status == 401) {
      const refreshToken = localStorage.getItem("refresh_token");

      if (!refreshToken) {
        localStorage.removeItem("access_token");

        return { status: "error", message: "No refresh token" };
      }

      const refreshRes = await fetch("http://127.0.0.1:5000/api/auth/refresh", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          Authorization: `Bearer ${refreshToken}`,
        },
      });

      if (refreshRes.ok) {
        const data = await refreshRes.json();
        localStorage.setItem("access_token", data.access_token);

        response = await fetch(url, {
          ...options,
          headers: {
            Authorization: `Bearer ${data.access_token}`,
            ...options.headers,
          },
        });

        return { status: "success", data: await response.json() };
      } else {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        return { status: "unauthorized", message: "Invalid refresh token" };
      }
    }

    return { status: "success", data: await response.json() };
  } catch (err) {
    return { status: "error", message: err.message || err };
  }
};
