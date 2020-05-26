/* COLLAPSING METODY */
    $("#filters-placeTypes").on('shown.bs.collapse', function () {
        document.getElementById('filters-placeTypesArrow').classList.remove('fa-caret-right');
        document.getElementById('filters-placeTypesArrow').classList.add('fa-caret-up');
    });
    $("#filters-placeTypes").on('hidden.bs.collapse', function () {
        document.getElementById('filters-placeTypesArrow').classList.remove('fa-caret-up');
        document.getElementById('filters-placeTypesArrow').classList.add('fa-caret-right');
    });
    $("#filters-Section").on('shown.bs.collapse', function () {
        document.getElementById('filters-ShowHideButton').innerText = "Hide filters";
        document.getElementById('filters-ButtonSeparator').hidden = false;
    });
    $("#filters-Section").on('hidden.bs.collapse', function () {
        document.getElementById('filters-ShowHideButton').innerText = "Show filters";
        document.getElementById('filters-ButtonSeparator').hidden = true;
    });

/* Rating input limitace na cisla 0 - 5 */
    $('.markInput').on('input', function() {
        if (this.value.length > 1) {
            this.value = this.value.slice(0, 1);
        }
        this.value = this.value.replace(/[^\d]/g, '');
        this.value = this.value.replace('6', '5');
        this.value = this.value.replace('7', '5');
        this.value = this.value.replace('8', '5');
        this.value = this.value.replace('9', '5');
    });