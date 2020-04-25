$(function () {
    for(var i = 0; i < 7; i++)
    {
        var e = document.getElementById('time' + i);
        if(!e.innerHTML.includes('-'))
        {
            e.innerHTML = 'no data';
        }
    }
});

function update(type) {
    document.getElementById('all-link').classList = "nav-link text-info";
    document.getElementById('positive-link').classList = "nav-link text-info";
    document.getElementById('negative-link').classList = "nav-link text-info";
    var place_id = 1;

    if(type == 1)
    {
        document.getElementById('all-link').classList = "nav-link active";
    }
    else if(type == 2)
    {
        document.getElementById('positive-link').classList = "nav-link active";
    }
    else if(type == 3)
    {
        document.getElementById('negative-link').classList = "nav-link active";
    }

    $.get( "/places/" + place_id + "/reviews/type/" + type, function( data ) {
        var content = "";
        var reviews = JSON.parse(data);
        reviews.forEach(review => {
            var rating = "";
            if(review.rating == 0)
            {
                rating = '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>';
            }
            else if(review.rating == 1)
            {
                rating = '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>';
            }
            else if(review.rating == 2)
            {
                rating = '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>';
            }
            else if(review.rating == 3)
            {
                rating = '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star-o"></i>\n' +
                    '<i class="fa fa-star-o"></i>';
            }
            else if(review.rating == 4)
            {
                rating = '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star-o"></i>';
            }
            else if(review.rating == 5)
            {
                rating = '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>\n' +
                    '<i class="fa fa-star"></i>';
            }
            content += '<div class="card m-2 my-3">\n' +
                '<div class="card-body">\n' +
                '<small class="float-right">' +
                rating +
                '</small>' +
                '<h2>' + review.user.username +'</h2>' +
                'rating: ' + review.rating +
                '<br>date posted: ' + review.time.slice(5,7) + '. ' + review.time.slice(8,10) + '. ' + review.time.slice(0,4) + ', ' + review.time.slice(11,16) + '. ' +
                '<br>review text: ' + review.text +
                '<br>' +
                '</div>' +
                '</div>';

        });
        $( "#card-content" ).html( content );
    });
}