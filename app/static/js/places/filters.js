var currentUrl = window.location.href.toLowerCase();
var filters = ['country=', 'city=', 'isverified=', 'isopen=', 'minrating=', 'maxrating='/*, 'placetype='*/];
var elementValue = "";

/* NAČÍTÁ AKTUÁLNÍ FILTRY DO HTML INPUTŮ */
    $(document).ready(function () {
        /* COUNTRY, CITY */
            for(var i = 0; i < 2; i++) {
                if (currentUrl.includes(filters[i])) {
                    elementValue = currentUrl.slice(currentUrl.indexOf(filters[i]) + (filters[i].length));
                    if (elementValue.indexOf('&') != -1) {
                        elementValue = elementValue.slice(0, elementValue.indexOf('&'));
                    }
                    if (i == 0) document.getElementById('filters-Country').value = elementValue;
                    else document.getElementById('filters-City').value = elementValue;
                }
            }

        /* VERIFIED */
            if (currentUrl.includes('isverified=true')) {
                document.getElementById('filters-Verified').checked = true;
            }

        /* OPENED */
            if (currentUrl.includes('isopen=true')) {
                document.getElementById('filters-OpenedState').checked = true;
            }

        /* MIN a MAX RATING */
            for(var i = 4; i < 6; i++) {
                if (currentUrl.includes(filters[i])) {
                    elementValue = currentUrl.slice(currentUrl.indexOf(filters[i]) + (filters[i].length), currentUrl.indexOf(filters[i]) + (filters[i].length) + 1);
                    if (i == 4 && elementValue != 0) document.getElementById('filters-MinRating').value = elementValue;
                    else if (i == 5 && elementValue != 5) document.getElementById('filters-MaxRating').value = elementValue;
                }
            }
    })

/* VLASTNÍ FILTERING (mění URL podle vybraných filtrů) */
    function filter() {
        var ordering = "";
        var filtersUrl = "";
        var orderingButtonText = document.getElementById('orderingButton').innerText;
        var filterValues = ["", "", "", "", "", ""];
                /* indexes:   [0]   country (string)
                              [1]   city (string)
                              [2]   isVerified ("true"/"")
                              [3]   isOpen ("true"/"")
                              [4]   minRating ("1" - "5")
                              [5]   maxRating ("0" - "4")
                 */

        /* získá jednotlivé vstupy filtrů */
            filterValues[0] = document.getElementById('filters-Country').value.toLowerCase();
            filterValues[1] = document.getElementById('filters-City').value.toLowerCase();
            if(document.getElementById('filters-Verified').checked) {
                filterValues[2] = "true";
            }
            if(document.getElementById('filters-OpenedState').checked) {
                filterValues[3] = "true";
            }
            if(document.getElementById('filters-MinRating').value != 0) {
                filterValues[4] = document.getElementById('filters-MinRating').value;
            }
            if(document.getElementById('filters-MaxRating').value != 5) {
                filterValues[5] = document.getElementById('filters-MaxRating').value;
            }
            /* PLACETYPES */

        /* VYPLIVNE ERROR POKUD JE MIN-RATING VĚTŠÍ NEŽ MAX-RATING */
            if(filterValues[4] > filterValues[5]) {
                return window.alert("Maximum rating is higher than minimum rating!");
            }

        /* zjistí aktuální typ řazení */
            if(currentUrl.includes('orderby='))
            {
                switch (orderingButtonText) {
                    case 'Z - A': ordering = 'name+desc'; break;
                    case 'A - Z': ordering = 'name'; break;
                    case 'Top rated': ordering = 'rating+desc'; break;
                    case 'Worst rated': ordering = 'rating'; break;
                    case 'Most rated': ordering = 'reviewcount+desc'; break;
                    case 'Least rated': ordering = 'reviewcount'; break;
                }
                ordering = '&orderby=' + ordering;
            }

        /* změní URL podle vlastních filtrů */
            filterValues.forEach(function (filterValue, i) {
                if(filterValue)
                {
                    filtersUrl += '&' + filters[i] + filterValue;
                }
            })
            window.location = '/places/?page=1' + ordering + filtersUrl;
    }