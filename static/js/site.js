document.addEventListener("click", (event) => {
  const closeButton = event.target.closest(".message-close");
  if (closeButton) {
    closeButton.closest(".message").remove();
  }
});

document.addEventListener("submit", (event) => {
  const message = event.target.dataset.confirm;
  if (message && !window.confirm(message)) {
    event.preventDefault();
  }
});
