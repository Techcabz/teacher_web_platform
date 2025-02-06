export function isString(input) {
  const regex = /^[a-zA-Z\s]{2,50}$/;
  return regex.test(input);
}

export function isMString(input) {
  const regex = /^[a-zA-Z\s]{0,50}$/;
  return regex.test(input);
}

export function isValidMiddleName(input) {
  const regex = /^[a-zA-Z\s]{0,50}$/;
  return regex.test(input);
}

export function isValidAge(age) {
  const regex = /^[0-9]+$/;
  return regex.test(String(age)) && age >= 8 && age <= 120;
}

export function isValidPassword(password) {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
  return regex.test(password);
}

export function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function validatePhoneNumber(phoneNumber) {
  const phoneNumberRegex = /^(?:\+639|09)\d{9}$/;
  return phoneNumberRegex.test(phoneNumber);
}


export function showErrorMessage(errorElement, field, message) {
  errorElement.innerHTML = message;
  field.classList.add("is-invalid");
}

export function hideErrorMessage(errorElement, field) {
  errorElement.innerHTML = "";
  field.classList.remove("is-invalid");
}

export const generateCodeString = () => {
  const chars = "0123456789";
  let result = "";
  for (let i = 0; i < 6; i++) {
    const randomIndex = Math.floor(
      (window.crypto.getRandomValues(new Uint32Array(1))[0] /
        (0xffffffff + 1)) *
        chars.length
    );
    result += chars[randomIndex];
  }
  return result;
};


export function alert(icon, position, title) {
  const Toast = Swal.mixin({
    toast: true,
    position: position,
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  });

  Toast.fire({
    icon: icon,
    title: title,
  });
}

export function showConfirmationDialog(title, confirmText, denyText, onConfirm, onDeny) {
  Swal.fire({
    title: title,
    showCancelButton: true,
    confirmButtonText: confirmText,
    denyButtonText: denyText,
  }).then((result) => {
    if (result.isConfirmed) {
      if (typeof onConfirm === "function") onConfirm();
    } else if (result.isDenied) {
      if (typeof onDeny === "function") onDeny();
    }
  });
}


export function setLoadingState(button, isLoading) {
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