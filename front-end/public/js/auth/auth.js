/*--------------------------- Post User Data --------------------------- */
export const registerUser = async (
  first_name,
  last_name,
  email,
  password,
  confirmation_password
) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/auth/register", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        first_name: first_name,
        last_name: last_name,
        email: email,
        password: password,
        confirmation_password: confirmation_password,
      }),
    });

    if (!response.ok) {
      return {
        status: "error",
        message: `HTTP Error: ${response.status}`,
      };
    }

    return await response.json();
  } catch (err) {
    return {
      status: "error",
      message: err,
    };
  }
};

export const loginUser = async (email, password, token) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    if (!response.ok) {
      return {
        status: "error",
        message: `HTTP Error: ${response.status}`,
      };
    }

    return await response.json();
  } catch (err) {
    return {
      status: "error",
      message: err,
    };
  }
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
      window.location.assign(
        "http://127.0.0.1:3000/public/pages/dashboard.html"
      );
    }
  });
};
