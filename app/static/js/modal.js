import {
  showErrorMessage,
  hideErrorMessage,
  isValidPassword,
  isString,
  isMString,
  alert,
  generateCodeString,
  validatePhoneNumber,
  showConfirmationDialog,
  setLoadingState,
} from "./main.module.js";

const categoryForm = document.querySelector("#categoryForm");
if (categoryForm) {
  categoryForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const categoryButton = document.querySelector("#categoryButton");
    const form = document.getElementById("categoryForm");
    const authError = form.querySelector("#cinameError");
    const categoryInput = form.querySelector("#ciname");

    if (!authError) {
      console.error("Error: cinameError element not found!");
      return;
    }

    setLoadingState(categoryButton, true);

    const cinameValue = formData.get("ciname");

    if (!cinameValue) {
      showErrorMessage(authError, categoryInput, "Input is required.");
      setLoadingState(categoryButton, false);
      return;
    } else {
      hideErrorMessage(authError, categoryInput);
    }

    // if (!isString(cinameValue)) {
    //     showErrorMessage(authError, categoryInput, "Invalid category name. Only letters & spaces allowed.");
    //     setLoadingState(categoryButton, false);
    //     return;
    // } else {
    //     hideErrorMessage(authError, categoryInput);
    // }

    try {
      const response = await fetch("/admin/category", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.href = "/admin/category";
        }, 2000);
      } else {
        showErrorMessage(authError, categoryInput, data.message);
        alert("warning", "top", data.message);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An unexpected error occurred.");
    } finally {
      setLoadingState(categoryButton, false);
    }
  });
}

const categoryFormUpdate = document.querySelector("#categoryFormUpdate");
if (categoryFormUpdate) {
  categoryFormUpdate.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const form = document.getElementById("categoryFormUpdate");
    const authError = form.querySelector("#cinameError");
    const categoryInput = form.querySelector("#ciname");

    const button = document.querySelector("#categoryButtonUpdate");

    setLoadingState(button, true);
    const id = formData.get("cid");

    const cinameValue = formData.get("ciname");
    if (!cinameValue) {
      showErrorMessage(authError, categoryInput, "Input is required.");
      setLoadingState(button, false);
      return;
    } else {
      hideErrorMessage(authError, categoryInput);
    }

    try {
      const response = await fetch(`/admin/category/${id}`, {
        method: "PUT",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.href = "/admin/category";
        }, 2000);
      } else {
        showErrorMessage(authError, categoryInput, data.message);
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An unexpected error occurred.");
      setLoadingState(button, false);
    }
  });
}
async function showUpdateForm(id) {
  document.getElementById("updateCategory").querySelector("#cid").value = id;
  try {
    const response = await fetch(`/admin/category/${id}`, { method: "GET" });

    if (!response.ok) {
      throw new Error("Failed to fetch category item.");
    }

    const data = await response.json();
    const form = document.getElementById("categoryFormUpdate");

    form.querySelector("#ciname").value = data.name || "";
    form.querySelector("#cid").value = data.id || "";

    const keywordContainer = document.getElementById("keywordsContainerUpdate");
    keywordContainer.innerHTML = "";

    // Populate keywords dynamically
    if (data.keywords && Array.isArray(data.keywords)) {
      data.keywords.forEach(keyword => addKeywordUpdate(keyword));
    }

    var updateModal = new bootstrap.Modal(
      document.getElementById("updateCategory")
    );
    updateModal.show();
  } catch (error) {
    console.error("Error:", error);
    alert("error", "top", "An unexpected error occurred.");
  }
}


async function deleteCategory(id) {
  showConfirmationDialog(
    "Are you sure you want to delete this category?",
    "Delete",
    "Cancel",
    async () => {
      try {
        const response = await fetch(`/admin/category/${id}`, {
          method: "DELETE",
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Failed to delete category.");
        }

        alert("success", "top", data.message);
        location.reload();
      } catch (error) {
        console.error("Error:", error);
        alert("error", "top", error.message);
      }
    },
    () => {
      alert("info", "top", "Category deletion was canceled.");
    }
  );
}

const uploadForm = document.querySelector("#uploadForm");
if (uploadForm) {
  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const button = document.querySelector("#uploadButton");
    const form = document.getElementById("uploadForm");
    const authError = form.querySelector("#docs_fileError");
    const input = form.querySelector("#docs_file");

    if (!authError) {
      console.error("Error: error element not found!");
      return;
    }

    setLoadingState(button, true);

    const docs_fileValue = formData.get("docs_file");

    if (!docs_fileValue) {
      showErrorMessage(authError, input, "Input is required.");
      setLoadingState(button, false);
      return;
    } else {
      hideErrorMessage(authError, input);
    }

    try {
      const response = await fetch("/admin/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.href = "/user/docs";
        }, 2000);
      } else {
        showErrorMessage(authError, input, data.message);
        alert("warning", "top", data.message);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An unexpected error occurred.");
    } finally {
      setLoadingState(button, false);
    }
  });
}

// dom calling
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".edit-category").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      const name = this.dataset.name;
      showUpdateForm(id, name);
    });
  });

  document.querySelectorAll(".delete-category").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      deleteCategory(id);
    });
  });

  document.querySelectorAll(".delete-file").forEach(button => {
    button.addEventListener("click", function () {
      let fileId = this.getAttribute("data-file-id");

      if (confirm("Are you sure you want to delete this file?")) {
        fetch(`/admin/delete_file/${fileId}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json"
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert("success", "top", data.message);
       
            location.reload();
          } else {
            alert("warning", "top", data.message);
          }
        })
        .catch(error => {
          console.error("Error:", error);
        });
      }
    });
  });

});
