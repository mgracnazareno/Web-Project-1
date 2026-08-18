const filterControls =document.querySelectorAll(".search-filters select, .search-filters input[type=checkbox]");

filterControls.forEach(function (control) {
    control.addEventListener("change", function () {
        this.form.submit();
    })
})

const bookModal = document.getElementById("bookModal");

if (bookModal) {
  bookModal.addEventListener("show.bs.modal", (event) => {
    const trigger = event.relatedTarget;
    document.getElementById("modalWhen").textContent = trigger.dataset.slotWhen;
    document.getElementById("bookForm").action = trigger.dataset.slotUrl;
  });
}