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

export const loginUser = async (email, password) => {
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
