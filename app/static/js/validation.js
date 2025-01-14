var notyf = new Notyf();

const registerForm = document.querySelector("#registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const registerButton = document.querySelector("#registerButton");
    setLoadingState(registerButton, true);

    try {
      const response = await fetch("/register", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/login";
        });

        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(registerButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(registerButton, false);
    }
  });
}

const loginForm = document.querySelector("#loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const loginButton = document.querySelector("#loginButton");
    setLoadingState(loginButton, true);

    try {
      const response = await fetch("/login", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        const notification = notyf.success(data.message);
        notification.on("click", ({ target, event }) => {
          window.location.href = "/admin/dashboard";
        });

        setTimeout(() => {
          window.location.href = "/admin/dashboard";
        }, 2000);
      } else {
        notyf.error(data.message);
        setLoadingState(loginButton, false);
      }
    } catch (error) {
      console.error("Error:", error);
      notyf.error("An unexpected error occurred.");
      setLoadingState(loginButton, false);
    }
  });
}

function setLoadingState(button, isLoading) {
  if (isLoading) {
    const loadingText = button.getAttribute("data-loading-text");
    button.setAttribute("data-original-text", button.textContent);
    button.textContent = loadingText;
    button.disabled = true;
    button.classList.add("opacity-50", "cursor-not-allowed");
  } else {
    button.textContent = button.getAttribute("data-original-text");
    button.removeAttribute("data-original-text");
    button.disabled = false;
    button.classList.remove("opacity-50", "cursor-not-allowed");
  }
}
