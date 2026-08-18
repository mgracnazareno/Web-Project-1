const filterControls =document.querySelectorAll(".search-filters select, .search-filters input[type=checkbox]");

filterControls.forEach(function (control) {
    control.addEventListener("change", function () {
        this.form.submit();
    })
})