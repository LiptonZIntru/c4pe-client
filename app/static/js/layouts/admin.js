/* kontroluje aktivní item v admin navbaru podle url */
    $(document).ready(
        function()
        {
            var userId = document.getElementById('userId').value;
            document.getElementsByTagName("body")[0].style.height = "50px";
            if (document.baseURI.endsWith('/admin/'))
            {
                document.getElementById('adminPagesLink').classList.add('active');
            }
            else if (document.baseURI.includes('/admin/places'))
            {
                document.getElementById('adminPlacesLink').classList.add('active');
            }
            else if (document.baseURI.includes('/admin/users'))
            {
                document.getElementById('adminUsersLink').classList.add('active');
            }
            else if (document.baseURI.includes('/admin/placetypes'))
            {
                document.getElementById('adminPlaceTypesLink').classList.add('active');
            }
        });