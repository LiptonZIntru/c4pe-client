var currentUrl = window.location.href.toLowerCase();

/* načte podle URL aktuání ordering do dropdownu */
    $(document).ready( function() {
        var innerText = "Order by";
        if(currentUrl.includes('orderby=name+desc')) innerText = 'Z - A';
        else if(currentUrl.includes('orderby=name')) innerText = 'A - Z';
        else if(currentUrl.includes('orderby=rating+desc')) innerText = 'Top rated';
        else if(currentUrl.includes('orderby=rating')) innerText = 'Worst rated';
        else if(currentUrl.includes('orderby=reviewcount+desc')) innerText = 'Most rated';
        else if(currentUrl.includes('orderby=reviewcount')) innerText = 'Least rated';

        document.getElementById('orderingButton').innerText = innerText;
    })

/* upraví URL podle vybraného orderingu || PAMATUJE SI TO I FILTRY :) || */
    function OrderNow(input)
    {
        var currentFilter = "";
        var filters = "";
        var orderingValues = ['orderby=name+desc', 'orderby=name', 'orderby=rating+desc', 'orderby=rating', 'orderby=reviewcount+desc', 'orderby=reviewcount'];

        /* ODSTRANÍ PŘEDCHOZÍ ŘAZENÍ Z URL */
            for (var i = 0; i < 6; i++)
            {
                if(currentUrl.includes('?' + orderingValues[i])) {
                    currentUrl = currentUrl.replace('?' + orderingValues[i], '');
                }
                if(currentUrl.includes('&' + orderingValues[i])) {
                    currentUrl = currentUrl.replace('&' + orderingValues[i], '');
                }
            }

        /* ODSTRANÍ PAGINATION Z URL */
            if(currentUrl.includes('?page=')) {
                currentUrl = currentUrl.replace('?page=' + currentUrl.substr(currentUrl.indexOf('?page=') + 6, 1), '');
            }
            if(currentUrl.includes('&page=')) {
                currentUrl = currentUrl.replace('&page=' + currentUrl.substr(currentUrl.indexOf('&page=') + 6, 1), '');
            }

        /* EXTRAHUJE FILTRY Z URL */
            filters = currentUrl.slice(currentUrl.indexOf('/places/') + 8);
            if(filters.startsWith('?')) {
                filters = filters.replace('?', '&');
            }

        /* ZMĚNÍ TEXT UVNITŘ TLAČÍTKA PRO ŘAZENÍ */
            if(input.includes('name'))
            {
                currentFilter = "A - Z";
                if(input.includes('desc')) currentFilter = "Z - A";
            }
            else if(input.includes('rating'))
            {
                currentFilter = "Worst rated";
                if(input.includes('desc')) currentFilter = "Top rated";
            }
            else if(input.includes('reviewcount'))
            {
                currentFilter = "Least rated";
                if(input.includes('desc')) currentFilter = "Most rated";
            }
            document.getElementById('orderingButton').innerText = currentFilter;

        /* ZMĚNÍ URL PODLE VYBRANÉHO ŘAZENÍ */
            window.location = '?page=1&orderby=' + input + filters;
    }