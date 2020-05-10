/* kontroluje aktivní item v navbaru podle url */
    $(document).ready(
        function()
        {
            var userId = document.getElementById('userId').value;
            document.getElementsByTagName("body")[0].style.height = "50px";
            if (document.baseURI.includes('/places/'))
            {
                document.getElementById('placesLink').classList.add('active');
            }
            else if (document.baseURI.includes('/login/'))
            {
                document.getElementById('loginLink').classList.add('active');
            }
            else if (document.baseURI.includes('/register/'))
            {
                document.getElementById('registerLink').classList.add('active');
            }
            else if (document.baseURI.includes('/users/' + userId + '/'))
            {
                document.getElementById('users/' + userId + 'Link').style.color = "rgba(255,255,255,.9)";
            }
            else if (document.baseURI.includes('/admin'))
            {
                document.getElementById('adminLink').classList.add('active');
            }
        });

/* kontroluje barvu itemů navbaru při přejetí myší */
    function ColorLinkOnHover(itemId, color, mask)
    {
        var intColor = [0, 0, 0];
        if (color == 'black')
        {
            intColor = [0, 0, 0];
        }
        else if (color == 'white')
        {
            intColor = [255, 255, 255];
        }

        if (!document.getElementsByTagName("title")[0].baseURI.includes('/' + itemId))
        {
            document.getElementById(itemId + 'Link').style.color = "rgba(" + intColor[0] + "," + intColor[1] + "," + intColor[2] + ",." + mask + ")";
        }
    }