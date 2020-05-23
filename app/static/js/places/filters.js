var currentUrl = window.location.href.toLowerCase();
var filters = ['name=', 'country=', 'city=', 'isverified=', 'isopen=', 'minrating=', 'maxrating='];
var elementValue = "";

/* PŘIDÁ DO URL PAGINATION, POKUD TAM CHYBÍ */
    $(document).ready(function () {
        if(!currentUrl.includes('page=')) {
            currentUrl = currentUrl.slice(currentUrl.indexOf('/places/') + '/places/'.length);
            if(currentUrl.startsWith('?')) {
                currentUrl = currentUrl.replace('?', '&');
            }
            window.location = '?page=1' + currentUrl;
        }
    })

/* NAČÍTÁ AKTUÁLNÍ FILTRY DO HTML INPUTŮ */
    $(document).ready(function () {
        /* COUNTRY, CITY */
            for(var i = 0; i < 3; i++) {
                if (currentUrl.includes(filters[i])) {
                    elementValue = currentUrl.slice(currentUrl.indexOf(filters[i]) + (filters[i].length));
                    if (elementValue.indexOf('&') != -1) {
                        elementValue = elementValue.slice(0, elementValue.indexOf('&'));
                    }
                    if (i == 1) document.getElementById('filters-Country').value = elementValue;
                    else if (i == 2) document.getElementById('filters-City').value = elementValue;
                    else document.getElementById('searchField').value = elementValue;
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
            for(var i = 5; i < 7; i++) {
                if (currentUrl.includes(filters[i])) {
                    elementValue = currentUrl.slice(currentUrl.indexOf(filters[i]) + (filters[i].length), currentUrl.indexOf(filters[i]) + (filters[i].length) + 1);
                    if (i == 5 && elementValue != 0) document.getElementById('filters-MinRating').value = elementValue;
                    else if (i == 6 && elementValue != 5) document.getElementById('filters-MaxRating').value = elementValue;
                }
            }

        /* PLACETYPES */
            var tempElement = "";
            if(currentUrl.includes('placetype=[')) {
                currentUrl.slice(currentUrl.indexOf('placetype=[') + "placetype=[".length).slice(0, currentUrl.slice(currentUrl.indexOf('placetype=[') + "placetype=[".length).indexOf(']')).split(',').forEach(id => {
                    tempElement = document.getElementById(id);
                    if(tempElement.classList.contains('placeType')) {
                        tempElement.checked = (tempElement.id == id);
                    }
                })
            }
            else {
                document.getElementById("any").checked = true;
            }
    })

/* VLASTNÍ FILTERING (mění URL podle vybraných filtrů) */
    function filter() {
        var ordering = "";
        var filtersUrl = "";
        var placeTypeFilter = "";
        var counter = 0;
        var anyPlaceTypeChecked = false;
        var orderingButtonText = document.getElementById('orderingButton').innerText;
        var filterValues = ["", "", "", "", "", "", ""];
                /* indexes:   [0]   name (string)
                              [1]   country (string)
                              [2]   city (string)
                              [3]   isVerified ("true"/"")
                              [4]   isOpen ("true"/"")
                              [5]   minRating ("1" - "5")
                              [6]   maxRating ("0" - "4")
                 */

        /* získá jednotlivé vstupy filtrů */
            filterValues[0] = document.getElementById('searchField').value.toLowerCase();
            filterValues[1] = document.getElementById('filters-Country').value.toLowerCase();
            filterValues[2] = document.getElementById('filters-City').value.toLowerCase();

            if(document.getElementById('filters-Verified').checked) {
                filterValues[3] = "true";
            }
            if(document.getElementById('filters-OpenedState').checked) {
                filterValues[4] = "true";
            }

            filterValues[5] = document.getElementById('filters-MinRating').value;
            filterValues[6] = document.getElementById('filters-MaxRating').value;

            document.querySelectorAll('.placeType').forEach(element => {
                if(element.id == "any" && element.checked) {
                    anyPlaceTypeChecked = true;
                }
                else if (counter == 0 && element.checked) {
                    placeTypeFilter = element.id.toString();
                    counter++;
                }
                else if (element.checked) {
                    placeTypeFilter = placeTypeFilter + ',' + element.id.toString();
                }
            })
            if(anyPlaceTypeChecked) placeTypeFilter = "";

        /* ERORRY */
            /* minrating > maxrating */
                if(filterValues[5] > filterValues[6]) {
                    return window.alert("Maximum rating is higher than minimum rating!");
                }

            /* string input obsahuje '&' */
                for (var i = 0; i < 3; i++) {
                    if(filterValues[i].includes('&')) return window.alert("Character '&' is not allowed to filter by.");
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
                    if((i == 5 && filterValue == 0) || (i == 6 && filterValue == 5)) {}
                    else {
                        filtersUrl += '&' + filters[i] + filterValue;
                    }
                }
            })
            if(placeTypeFilter) {
                filtersUrl += ('&placetype=[' + placeTypeFilter + ']');
            }

            window.location = '/places/?page=1' + ordering + filtersUrl;
    }