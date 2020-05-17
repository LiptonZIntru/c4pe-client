/* Kontroluje heslo */
    $('#register').submit(function (e) {
        if($('#password').val() != $('#confirmation').val())
        {
            e.preventDefault(); // TODO: raise password doesn't match error
            alert("Passwords doesn't match");
        }
        if($('#password').val().length < 8)
        {
            e.preventDefault();
            alert("Password must contain 8 or more characters");
        }
    })