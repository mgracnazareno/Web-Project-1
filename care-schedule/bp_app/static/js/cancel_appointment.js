document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("cancelAppointmentModal");
    if (!modal) return;

    const form = modal.querySelector("[data-cancel-form]");
    const when = modal.querySelector("[data-cancel-when]");

    // One modal serves every row, so fill it from the button that opened it
    modal.addEventListener("show.bs.modal", (event) => {
        const trigger = event.relatedTarget;
        if (!trigger) return;

        form.action = trigger.dataset.cancelUrl;
        when.textContent = trigger.dataset.apptWhen;
    });
});