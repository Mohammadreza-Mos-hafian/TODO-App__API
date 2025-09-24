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

export const showErrorMessage = (errors = {}) => {
  document.querySelectorAll(".error-message").forEach((elem) => {
    elem.textContent = "";
    elem.classList.remove("text-danger");
  });

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
