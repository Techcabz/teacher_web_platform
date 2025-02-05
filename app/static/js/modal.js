import {
  showErrorMessage,
  hideErrorMessage,
  isValidPassword,
  isString,
  isMString,
  alert,
  generateCodeString,
  validatePhoneNumber,
  setLoadingState,
} from "./main.module.js";

const categoryForm = document.querySelector("#categoryForm");

if (categoryForm) {
  categoryForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const categoryButton = document.querySelector("#categoryButton");
    const authError = document.getElementById("cinameError");
    const categoryInput = document.querySelector('[name="ciname"]');

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
