// Delete Availability Slot modal: one modal shared by every slot row.

(function () {
    "use strict";

    const deleteSlotModal = document.getElementById("deleteSlotModal");

    // Nothing to wire up if the delete modal isn't on this page
    if (!deleteSlotModal) return;

    deleteSlotModal.addEventListener("show.bs.modal", function (event) {
        const trash = event.relatedTarget;

        deleteSlotModal.querySelector("form").action = trash.dataset.action;
        deleteSlotModal.querySelector("#deleteSlotName").textContent = trash.dataset.slot;
    });

})();