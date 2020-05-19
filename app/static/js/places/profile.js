var newStars = ['oneStar', 'twoStar', 'threeStar', 'fourStar', 'fiveStar'];
var editStars = ['oneS', 'twoS', 'threeS', 'fourS', 'fiveS'];
var freezed = false;
var rating = 0;

/* ZOBRAZÍ "NO DATA" OTEVÍRACÍ DOBU PRO NEDOSTUPNÉ ČASY */
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

/* ZOBRAZÍ "NEW REVIEW" BUTTON, POKUD UŽIVATEL JE OPRÁVNĚNÝ */
    $(document).ready(function(){
        var user_id = document.getElementById('user_id').value;
        var place_id = document.getElementById('page_id').value;
        var isCurrent = false;
        $.get( "/places/" + place_id + '/reviews/type/1', function ( data ) {
            var reviews = JSON.parse(data);
            reviews.forEach(review => {
                if (review.user.id == user_id)
                {
                    isCurrent = true;
                }
            })

            if(!isCurrent)
            {
                document.getElementById('newReviewButton').hidden = false;
            }
        })
    })

/* VYKRESLUJE HVĚZDY PŘI PSANÍ NOVÉ RECENZE */
    function colorStars(method, element) {
        if(method == 'edit')
        {
            if(!freezed) {
                for (var i = 5; i < editStars.length; i++) {
                    document.getElementById(editStars[i]).classList = "fa fa-star-o";
                }
                if (element.id == 'oneS') {
                    rating = 1;
                } else if (element.id == 'twoS') {
                    rating = 2;
                } else if (element.id == 'threeS') {
                    rating = 3;
                } else if (element.id == 'fourS') {
                    rating = 4;
                } else if (element.id == 'fiveS') {
                    rating = 5;
                }
                for (var i = 0; i < rating; i++) {
                    document.getElementById(editStars[i]).classList = "fa fa-star";
                }
            }
        }
        else
        {
            if(!freezed) {
                for (var i = 0; i < newStars.length; i++) {
                    document.getElementById(newStars[i]).classList = "fa fa-star-o";
                }
                if (element.id == 'oneStar') {
                    rating = 1;
                } else if (element.id == 'twoStar') {
                    rating = 2;
                } else if (element.id == 'threeStar') {
                    rating = 3;
                } else if (element.id == 'fourStar') {
                    rating = 4;
                } else if (element.id == 'fiveStar') {
                    rating = 5;
                }
                for (var i = 0; i < rating; i++) {
                    document.getElementById(newStars[i]).classList = "fa fa-star";
                }
            }
        }

    }

/* ULOŽÍ ZVOLENÝ POČET HVĚZD PŘI KLIKU */
    function saveRating(id)
    {
        if(!freezed)
        {
            document.getElementById(id).value = rating;
            freezed = true;
        }
        else
        {
            freezed = false;
        }
    }

/* PSANÍ RECENZE */
    function updateText(target, source) {
        document.getElementById(target).value = document.getElementById(source).value;
    }

/* COLLAPSING */
    $("#newReviewForm").on('show.bs.collapse', function(){
        document.getElementById('buttonCollapse').innerText = "Close your review";
      });
    $("#newReviewForm").on('hide.bs.collapse', function(){
        document.getElementById('buttonCollapse').innerText = "Write a review!";
      });

/* ZAMODRÁVÁNÍ LIKE/DISLIKE BUTTONU */
    function blueThis(id)
    {
        document.getElementById(id).classList.toggle("text-primary");
        document.getElementById(id).classList.toggle("text-secondary");
    }

/* LIKE/DISLIKE RECENZE */
    function likeReview(userID, placeID, reviewID) {
        /*
        * if review has like
        *
        */
        $.get('/places/' + placeID + '/reviews/' + reviewID + '/like/', function (data) {
            // success = review liked
            // vybarvit/odbarvit like tlacitko
            alert(data);
        });
    }
    function dislikeReview(userID, placeID, reviewID) {
        $.get('/places/' + placeID + '/reviews/' + reviewID + '/dislike/', function (data) {
            // success = review disliked
            // vybarvit/odbarvit dislike tlacitko
            alert(data);
        });
    }

/* EDITACE RECENZE */
    function editReview(place_id, review_id)
    {
        var reviewForm = document.getElementById('editReview');
        var staticReview = document.getElementById('review-Content');
        var editReviewButton = document.getElementById('editReviewButton');
        var staticRating = document.getElementById('staticRating');
        var editRating = document.getElementById('editRating');

        if(editReviewButton.innerText == "Edit")
        {
            editReviewButton.innerText = 'Save';
            staticReview.hidden = true;
            reviewForm.hidden = false;
            staticRating.hidden = true;
            editRating.hidden = false;
        }
        else
        {
            editReviewButton.setAttribute('form', 'editReview');
            reviewForm.action = '/places/' + place_id + '/reviews/' + review_id + '/edit/';
            editReviewButton.type = 'submit';
        }
    }