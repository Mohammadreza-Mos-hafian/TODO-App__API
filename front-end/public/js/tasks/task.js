/*--------------------------- Post Task Data --------------------------- */
export const createTask = async (title, deadline, description = "") => {
  try {
    const response = await fetch("http://localhost:5000/api/tasks/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({
        title: title,
        deadline: deadline,
        description: description,
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


