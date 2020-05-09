/* FILTR RECENZÍ (navigation bar) */
    function update(type) {
        document.getElementById('all-link').classList = "nav-link text-primary";
        document.getElementById('positive-link').classList = "nav-link text-primary";
        document.getElementById('negative-link').classList = "nav-link text-primary";
        document.getElementById('verified-link').classList = "nav-link text-primary";
        var place_id = document.getElementById('page_id').value;

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
        else if(type == 4)
        {
            document.getElementById('verified-link').classList = "nav-link active";
        }

        $.get( "/places/" + place_id + "/reviews/type/" + type, function( data ) {
            var content = "";
            var reviews = JSON.parse(data);
            reviews.forEach(review => {
                var rating = "";
                var user_icon = '';
                var review_time = review.time.slice(5,7) + "." + review.time.slice(8,10) + "." + review.time.slice(0,4) + ' ' +
                    review.time.slice(11,16);
                if(review.user.isVerified == 1)
                {
                    user_icon = '<i class="fas fa-check-circle" style="color:green; padding-top: 1.4%" data-toggle="tooltip" data-placement="bottom" title="User is verified"></i> '
                }
                for(var i = 0; i < review.rating; i++)
                {
                    rating += '<i class="fa fa-star"></i> ';
                }
                for(var i = 0; i < 5 - review.rating; i++)
                {
                    rating += '<i class="fa fa-star-o"></i> ';
                }
                content += '<div class="card m-2 mt-1 mb-3">' +
                    '<div class="card-body pb-2 pt-2">' +
                    '<small class="float-right pt-2">' +
                    rating +
                    '</small>' +
                    '<p class="text-nowrap mb-2">User ' +
                    user_icon +
                    '<a href="/users/' + review.user.id + '" class="text-dark"><b>' + review.user.username + '</b></a>' +
                    ' says:' +
                    '</p>' +
                    '<div class="card p-2 pl-3 text-justify" id="review-Content">' +
                    review.text +
                    '</div>' +
                    '<div class="row justify-content-between mb-0">' +
                    '<div class="col-auto mt-1 ml-2 row text-nowrap">' +
                    '<x class="defaultCursor">' +
                    review.positiveReactions +
                    '</x>' +
                    '<i class="fa fa-thumbs-up px-1 pt-1 text-secondary pointer" id="negativeReaction_' + review.id +
                    '" onmouseover="blueThis(this.id);" onmouseout="blueThis(this.id);" onclick="likeReview(' + currentUser.id + ', ' + place_id + ', ' + review.id + ');"></i>' +
                    '<y class="defaultCursor">' + review.negativeReactions + '</y>' +
                    '<i class="fa fa-thumbs-down pl-1 pt-1 text-secondary pointer" id="positiveReaction_' + review.id +
                    '" onmouseover="blueThis(this.id);" onmouseout="blueThis(this.id);" onclick="dislikeReview(' + currentUser.id + ', ' + place_id + ', ' + review.id + ');"></i>' +
                    '</div>' +
                    '<div class="col-auto">' +
                    '<p class="text-nowrap m-0 pt-1 float-right" style="font-size: smaller">' +
                    'Review added ' + review_time +
                    '</p>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</div>'

            });
            $( "#userReviews" ).html( content );
        });
    }
