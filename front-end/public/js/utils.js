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

export const showUserName = () => {
  if (localStorage.getItem("full_name")) {
    document.querySelector(".user-name").textContent =
      localStorage.getItem("full_name");
  }
};

export const showResult = (number, obj) => {
  const tableRow = document.createElement("tr");

  const tableData = `
  <td>${number}</td>
  <td>${obj.title}</td>
  <td><span class="badge text-bg-${obj.color}">${obj.status}</span></td>
  <td>${obj.deadline}</td>
  <td>
    <a href="../tasks/task_edit.html" class="btn btn-primary btn-sm">Edit</a>

    <a href="#" class="btn btn-danger btn-sm">Delete</a>

    <a href="../files/file_index.html" class="btn btn-secondary btn-sm">Files</a>
  </td>
  `;

  tableRow.innerHTML = tableData;

  return tableRow;
};

const renderPagination = (totalPages, activePage, perPage) => {
  const paginationContainer = document.getElementById("pagination");

  paginationContainer.innerHTML = "";

  const first = document.createElement("li");
  first.className = "page-item";
  first.innerHTML = `<a class="page-link text-bg-dark" href="#">&laquo;</a>`;
  first.addEventListener("click", () => loadTasks(1, perPage));
  paginationContainer.appendChild(first);

  const prev = document.createElement("li");
  prev.className = "page-item";
  prev.innerHTML = `<a class="page-link text-bg-dark" href="#">&lsaquo;</a>`;
  if (activePage > 1)
    prev.addEventListener("click", () => loadTasks(activePage - 1, perPage));
  else prev.classList.add("disabled");
  paginationContainer.appendChild(prev);

  let startPage = activePage - 1;
  let endPage = activePage + 1;

  if (startPage < 1) {
    startPage = 1;
    endPage = Math.min(3, totalPages);
  }
  if (endPage > totalPages) {
    endPage = totalPages;
    startPage = Math.max(1, totalPages - 2);
  }

  for (let i = startPage; i <= endPage; i++) {
    const li = document.createElement("li");
    li.className = "page-item";
    if (i === activePage) li.classList.add("active");
    li.innerHTML = `<a class="page-link text-bg-dark" href="#">${i}</a>`;
    li.addEventListener("click", () => loadTasks(i, perPage));
    paginationContainer.appendChild(li);
  }

  const next = document.createElement("li");
  next.className = "page-item";
  next.innerHTML = `<a class="page-link text-bg-dark" href="#">&rsaquo;</a>`;
  if (activePage < totalPages)
    next.addEventListener("click", () => loadTasks(activePage + 1, perPage));
  else next.classList.add("disabled");
  paginationContainer.appendChild(next);

  const last = document.createElement("li");
  last.className = "page-item";
  last.innerHTML = `<a class="page-link text-bg-dark" href="#">&raquo;</a>`;
  last.addEventListener("click", () => loadTasks(totalPages, perPage));
  paginationContainer.appendChild(last);
};

export const loadTasks = async (page = 1, perPage = 5) => {
  const table = document.querySelector(".table tbody");
  const hiddenRow = document.getElementById("hiddenRow");

  try {
    const response = await apiRequest(
      `http://127.0.0.1:5000/api/tasks?page=${page}&per_page=${perPage}`,
      { method: "GET" }
    );

    const tasks = response.data?.tasks || [];
    const totalPages = response.data?.total_pages || 1;

    if (tasks.length !== 0) {
      table.innerHTML = "";

      let index = (page - 1) * perPage;

      tasks.forEach((obj) => {
        table.appendChild(showResult(index + 1, obj));
        index++;
      });

      renderPagination(totalPages, page, perPage);
    } else {
      if (hiddenRow) hiddenRow.classList.remove("d-none");
    }
  } catch (err) {
    console.error("Unexpected error:", err);
  }
};
