// Edit Availability Slot modal: one modal shared by every slot row.

(function () {
    "use strict";

    const editSlotModal = document.getElementById("editSlotModal");

    // Nothing to wire up if the edit modal isn't on this page
    if (!editSlotModal) return;

    // the button that triggered it
    editSlotModal.addEventListener("show.bs.modal", function (event) {
        const pencil = event.relatedTarget;
        const form = editSlotModal.querySelector("form");

        // The inputs only accept these formats, which is why the template
        // writes the values as %Y-%m-%d and %H:%M
        form.action = pencil.dataset.action;
        form.querySelector('[name="date"]').value = pencil.dataset.date;
        form.querySelector('[name="start_time"]').value = pencil.dataset.start;
        form.querySelector('[name="end_time"]').value = pencil.dataset.end;
    });

})();