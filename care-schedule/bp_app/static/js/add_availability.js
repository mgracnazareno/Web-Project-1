// Availability page — add-slot rows and the edit modal.

(function () {
    "use strict";

    const slotRowTemplate = document.getElementById("slotRowTemplate");
    const slotRows = document.getElementById("slotRows");
    const addRowBtn = document.getElementById("addRowBtn");

    if (!slowRowTemplate) return;

    // Disable the remove button when only one row is left,
    // so the form can never end up with zero times
    function refreshRemoveButtons() {
        const rows = slotRows.querySelectorAll(".slot-row");
        rows.forEach(function (row) {
            row.querySelector(".remove-row").disabled = rows.length === 1;
        });
    }

    // Clone the template's content and drop it into the container
    function addSlotRow() {
        slotRows.appendChild(slotRowTemplate.content.cloneNode(true));
        refreshRemoveButtons();
    }

    addRowBtn.addEventListener("click", addSlotRow);

    // One listener on the container handles every row, even future ones
    slotRows.addEventListener("click", function (event) {
        const button = event.target.closest(".remove-row");
        if (!button) return;

        button.closest(".slot-row").remove();
        refreshRemoveButtons();
    });

    // Start the add form off with one empty row
    addSlotRow();
})













