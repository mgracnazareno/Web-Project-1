// Enable the confirm button and show the chosen time in the footer bar
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("rescheduleForm");
  if (!form) return;

  const selectedText = document.getElementById("rsSelected");
  const confirmButton = document.getElementById("rsConfirm");

  form.addEventListener("change", function (event) {
    if (event.target.name !== "availability_id") return;
    selectedText.textContent = event.target.dataset.slotWhen;
    selectedText.classList.add("is-chosen");
    confirmButton.disabled = false;
  });
});