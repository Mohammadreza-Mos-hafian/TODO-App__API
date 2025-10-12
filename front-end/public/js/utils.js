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

  document.querySelector(".alert").classList.add("d-none")
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

/*--------------------------- Pagination --------------------------- */

const showTaskStatus = (number) => {
  const statuses = ["Pending", "In progress", "Completed", "Canceled"];

  for (const status of statuses) {
    if (status === statuses[number]) {
      return status;
    }
  }
};

const templates = {
  tasks: (n, o) => `
    <td>${n}</td>
    <td>${o.title}</td>
    <td>
      <span class="badge text-bg-${o.color}">
        ${showTaskStatus(o.status)}
      </span>
    </td>
    <td>${o.deadline}</td>
    <td>
      <a 
        href="../tasks/task_edit.html?uuid=${o.uuid}" 
        class="btn btn-primary btn-sm">Edit
      </a>
      <a
        class="btn btn-danger btn-sm delete-btn" 
        data-task-uuid="${o.uuid}">Delete
      </a>
      <a 
        href="../files/file_index.html?uuid=${o.uuid}" 
        class="btn btn-secondary btn-sm">Files
      </a>
    </td>
  `,
  files: (n, o) => `
    <td>${n}</td>
    <td>${o.original_name}</td>
    <td>
      <a
        class="btn btn-primary btn-sm download-btn"
        data-file-uuid="${o.uuid}">Download
      </a>
      <a 
        class="btn btn-danger btn-sm delete-btn" 
        data-file-uuid="${o.uuid}">Delete
      </a>
    </td>
  `,
};

export const showResult = (number, obj, pageName) => {
  const row = document.createElement("tr");
  row.innerHTML = templates[pageName]?.(number, obj) || "";
  return row;
};

const createButton = (label, disabled, onClick, isActive = false) => {
  const li = document.createElement("li");
  li.className = `page-item ${disabled ? "disabled" : ""} ${
    isActive ? "active" : ""
  }`;

  const a = document.createElement("a");
  a.className = "page-link text-bg-dark";
  a.href = "#";
  a.innerHTML = label;

  if (!disabled && onClick) a.addEventListener("click", onClick);

  li.appendChild(a);
  return li;
};

const renderPagination = (totalPages, activePage, perPage, pageName) => {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const addBtn = (label, disabled, onClick, isActive = false) =>
    pagination.appendChild(createButton(label, disabled, onClick, isActive));

  addBtn("&laquo;", activePage === 1, () => loadData(1, perPage, pageName));
  addBtn("&lsaquo;", activePage === 1, () =>
    loadData(activePage - 1, perPage, pageName)
  );

  const start = Math.max(1, activePage - 1);
  const end = Math.min(totalPages, activePage + 1);

  for (let i = start; i <= end; i++) {
    addBtn(i, false, () => loadData(i, perPage, pageName), i === activePage);
  }

  addBtn("&rsaquo;", activePage === totalPages, () =>
    loadData(activePage + 1, perPage, pageName)
  );
  addBtn("&raquo;", activePage === totalPages, () =>
    loadData(totalPages, perPage, pageName)
  );
};

export const loadData = async (page = 1, perPage = 5, pageName) => {
  const tableBody = document.querySelector(".table tbody");
  const hiddenRow = document.getElementById("hiddenRow");
  const taskNameElem = document.getElementById("taskName");

  let taskUuid = "";

  if (pageName == "files") {
    const params = new URLSearchParams(window.location.search);
    taskUuid = `&uuid=${params.get("uuid")}`;
  }

  try {
    const response = await apiRequest(
      `http://127.0.0.1:5000/api/${pageName}?page=${page}&per_page=${perPage}${taskUuid}`,
      { method: "GET" }
    );

    const dataKey = pageName;
    const data = response.data[dataKey] || [];
    const totalPages = response.data?.total_pages || 1;

    if (taskNameElem) taskNameElem.textContent = response.data.task_name;

    if (data.length) {
      tableBody.innerHTML = "";

      data.forEach((obj, index) => {
        const row = showResult((page - 1) * perPage + index + 1, obj, pageName);
        tableBody.appendChild(row);
      });

      hiddenRow?.classList.add("d-none");
      renderPagination(totalPages, page, perPage, pageName);
    } else {
      hiddenRow?.classList.remove("d-none");
    }
  } catch (err) {
    console.error("Error loading data:", err);
  }
};
