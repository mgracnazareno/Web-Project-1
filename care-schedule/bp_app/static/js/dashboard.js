/* ===========================================================
   static/js/dashboard.js
   Collapses the sidebar to an icon rail and remembers the
   choice, so it stays collapsed as you move between pages.
   =========================================================== */

const layout = document.getElementById("dashboardLayout");
const railToggle = document.getElementById("railToggle");
const railToggleIcon = document.getElementById("railToggleIcon");

const STORAGE_KEY = "careschedule-sidebar-rail";

function applyRail(isRailed) {
    layout.classList.toggle("rail", isRailed);
    railToggle.setAttribute("aria-expanded", String(!isRailed));
    railToggle.setAttribute(
        "aria-label",
        isRailed ? "Expand sidebar" : "Collapse sidebar"
    );
    railToggleIcon.className = isRailed
        ? "bi bi-chevron-double-right"
        : "bi bi-chevron-double-left";
}

// Restore the state saved on the last visit.
applyRail(localStorage.getItem(STORAGE_KEY) === "true");

railToggle.addEventListener("click", () => {
    const isRailed = !layout.classList.contains("rail");
    applyRail(isRailed);
    localStorage.setItem(STORAGE_KEY, String(isRailed));
});