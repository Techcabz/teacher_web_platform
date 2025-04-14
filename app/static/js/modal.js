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
    const authError = form.querySelector("#cunameError");
    const categoryInput = form.querySelector("#cuname");

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

    form.querySelector("#cuname").value = data.name || "";
    form.querySelector("#cid").value = data.id || "";

    const keywordContainer = document.getElementById("keywordsContainerUpdate");
    keywordContainer.innerHTML = "";

    // Populate keywords dynamically
    if (data.keywords && Array.isArray(data.keywords)) {
      data.keywords.forEach((keyword) => addKeywordUpdate(keyword));
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
    "Deleting this category will also remove all files associated with it. Are you sure you want to proceed?",
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

async function deleteUser(id) {
  showConfirmationDialog(
    "Deleting this user will also remove all files uploaded by them. This action is irreversible. Are you sure you want to proceed?",
    "Delete",
    "Cancel",
    async () => {
      try {
        const response = await fetch(`/admin/users/${id}`, {
          method: "DELETE",
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Failed to delete user.");
        }

        alert("success", "top", data.message);
        location.reload();
      } catch (error) {
        console.error("Error:", error);
        alert("error", "top", error.message);
      }
    },
    () => {
      alert("info", "top", "User deletion was canceled.");
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
    const progressContainer = document.querySelector("#progressContainer");
    const progressBar = document.querySelector("#uploadProgress");

    // Reset progress bar
    progressBar.style.width = "0%";
    progressBar.textContent = "0%";
    progressContainer.style.display = "block";

    if (!authError) {
      console.error("Error: error element not found!");
      return;
    }

    if (!input.files.length) {
      showErrorMessage(authError, input, "Input is required.");
      progressContainer.style.display = "none";
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

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/admin/upload", true);

    // Track upload progress
    xhr.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        const percent = Math.round((event.loaded / event.total) * 100);
        progressBar.style.width = percent + "%";
        progressBar.textContent = percent + "%";
      }
    });

    xhr.onload = function () {
      const data = JSON.parse(xhr.responseText);
      if (xhr.status === 200) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.href = "/user/docs";
        }, 2000);
      } else {
        showErrorMessage(authError, input, data.message);
        alert("warning", "top", data.message);
      }
      setLoadingState(button, false);
      progressContainer.style.display = "none";
    };

    xhr.onerror = function () {
      alert("error", "top", "An unexpected error occurred.");
      setLoadingState(button, false);
      progressContainer.style.display = "none";
    };

    // Send the file
    xhr.send(formData);
    // try {
    //   const response = await fetch("/admin/upload", {
    //     method: "POST",
    //     body: formData,
    //   });

    //   const data = await response.json();

    //   if (response.ok) {
    //     alert("success", "top", data.message);
    //     setTimeout(() => {
    //       window.location.href = "/user/docs";
    //     }, 2000);
    //   } else {
    //     showErrorMessage(authError, input, data.message);
    //     alert("warning", "top", data.message);
    //   }
    // } catch (error) {
    //   console.error("Error:", error);
    //   alert("error", "top", "An unexpected error occurred.");
    // } finally {
    //   setLoadingState(button, false);
    // }
  });
}

const profileFormUserAdmin = document.querySelector("#profileFormUserAdmin");
if (profileFormUserAdmin) {
  profileFormUserAdmin.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileFormUserAdmin.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/admin/update_profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

const profileFormEditAdmin = document.querySelector("#profileFormEditAdmin");
if (profileFormEditAdmin) {
  profileFormEditAdmin.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileFormEditAdmin.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/admin/update_profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

const profileForm = document.querySelector("#profileForm");
if (profileForm) {
  profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = profileForm.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/user/update_profile_sc", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

const addAdminModal = document.querySelector("#addAdminModal");
if (addAdminModal) {
  addAdminModal.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formDataObject = Object.fromEntries(formData.entries());
    const button = addAdminModal.querySelector("button.btn-primary");

    setLoadingState(button, true);

    try {
      const response = await fetch("/user/add_admin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDataObject),
      });

      const data = await response.json();

      if (response.ok) {
        alert("success", "top", data.message);
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      } else {
        alert("warning", "top", data.message);
        setLoadingState(button, false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("error", "top", "An error occurred while updating your profile.");
      setLoadingState(button, false);
    }
  });
}

function showUpdateUser(id, name) {
  fetch(`/admin/get_profile_user/${id}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.success) {
        document.getElementById("profile_id").value = data.user.id;

        document.getElementById("asusername").value =
          data.user.username || "N/A";
        document.getElementById("asfname").value = data.user.firstname || "N/A";
        document.getElementById("asmname").value =
          data.user.middlename || "N/A";
        document.getElementById("aslname").value = data.user.lastname || "N/A";
        document.getElementById("asemail").value = data.user.email || "N/A";

        var updateModal = new bootstrap.Modal(
          document.getElementById("profileUserModal")
        );
        updateModal.show();
      } else {
        alert("warning", "top", "Failed to load profile data.");
      }
    })
    .catch((error) => {
      console.error("Error fetching profile data:", error);
      alert("warning", "top", "Error fetching profile data.");
    });
}

function showUpdateUsers(id, name) {
  fetch(`/admin/get_profile_admin/${id}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("profile_user_id").value = data.user.id;

        document.getElementById("ausername").value =
          data.user.username || "N/A";
        document.getElementById("afname").value = data.user.firstname || "N/A";
        document.getElementById("amname").value = data.user.middlename || "N/A";
        document.getElementById("alname").value = data.user.lastname || "N/A";
        document.getElementById("email").value = data.user.email || "N/A";

        var updateModal = new bootstrap.Modal(
          document.getElementById("profileUserAdminModal")
        );
        updateModal.show();
      } else {
        alert("warning", "top", "Failed to load profile data.");
      }
    })
    .catch((error) => {
      console.error("Error fetching profile data:", error);
      alert("warning", "top", "Error fetching profile data.");
    });
}
function showUpdateAdmin(id, name) {
  fetch(`/admin/get_profile_admin/${id}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("profile_admin_id").value = data.user.id;

        document.getElementById("adusername").value =
          data.user.username || "N/A";
        document.getElementById("adfname").value = data.user.firstname || "N/A";
        document.getElementById("admname").value =
          data.user.middlename || "N/A";
        document.getElementById("adlname").value = data.user.lastname || "N/A";

        var updateModal = new bootstrap.Modal(
          document.getElementById("profileAdminModal")
        );
        updateModal.show();
      } else {
        alert("warning", "top", "Failed to load profile data.");
      }
    })
    .catch((error) => {
      d;
      console.error("Error fetching profile data:", error);
      alert("warning", "top", "Error fetching profile data.");
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

  document.querySelectorAll(".delete-user").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      deleteUser(id);
    });
  });

  document.querySelectorAll(".edit-profile-user").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      const name = this.dataset.name;
      showUpdateUsers(id, name);
    });
  });
  document.querySelectorAll(".edit-users").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      const name = this.dataset.name;
      showUpdateUser(id, name);
    });
  });
  document.querySelectorAll(".edit-profile-admin").forEach((button) => {
    button.addEventListener("click", function () {
      const id = this.dataset.id;
      const name = this.dataset.name;
      showUpdateAdmin(id, name);
    });
  });

  document.querySelectorAll(".delete-file").forEach((button) => {
    button.addEventListener("click", function () {
      let fileId = this.getAttribute("data-file-id");

      if (
        showConfirmationDialog(
          "Are you sure you want to delete this file?",
          "Yes",
          "No"
        )
      ) {
        fetch(`/admin/delete_file/${fileId}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert("success", "top", data.message);

              location.reload();
            } else {
              alert("warning", "top", data.message);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    });
  });

  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("bUserA")) {
      let userID = event.target.getAttribute("data-user-id");

      showConfirmationDialog(
        "Are you sure you want to approved this user?",
        "Yes",
        "No",
        async () => {
          try {
            const response = await fetch(`/admin/users/approved/${userID}`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ status: 1 }),
            });

            const data = await response.json();

            if (!response.ok) {
              throw new Error(data.message);
            }

            alert("success", "top", data.message);
            window.location.reload();
          } catch (error) {
            console.error("Error:", error);
            alert("error", "top", error.message);
          }
        },
        () => {}
      );
    }

    if (event.target.classList.contains("bUserD")) {
      let userID = event.target.getAttribute("data-user-id");

      showConfirmationDialog(
        "Are you sure you want to disapprove this user? This will delete the user from our records. Do you want to continue?",
        "Yes",
        "No",
        async () => {
          try {
            const response = await fetch(`/admin/users/disapproved/${userID}`, {
              method: "DELETE",
              headers: { "Content-Type": "application/json" },
            });

            const data = await response.json();

            if (!response.ok) {
              throw new Error(data.message);
            }

            alert("success", "top", data.message);
            window.location.reload();
          } catch (error) {
            console.error("Error:", error);
            alert("error", "top", error.message);
          }
        },
        () => {}
      );
    }
  });
});
