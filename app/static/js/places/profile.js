$(function () {
    for(var i = 0; i < 7; i++)
    {
        var e = document.getElementById('time' + i);
        if(!e.innerHTML.includes('-'))
        {
            e.innerHTML = 'no data';
        }
    }
})