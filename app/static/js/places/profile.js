var stars = ['oneStar', 'twoStar', 'threeStar', 'fourStar', 'fiveStar'];
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
    function colorStars(element) {
        if(!freezed) {
            for (var i = 0; i < stars.length; i++) {
                document.getElementById(stars[i]).classList = "fa fa-star-o";
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
                document.getElementById(stars[i]).classList = "fa fa-star";
            }
        }
    }

/* ULOŽÍ ZVOLENÝ POČET HVĚZD PŘI KLIKU */
    function saveRating()
    {
        if(!freezed)
        {
            document.getElementById('rating').value = rating;
            freezed = true;
        }
        else
        {
            freezed = false;
        }
    }

/* PSANÍ RECENZE */
    function updateText() {
        document.getElementById('newReviewText').value = document.getElementById('newReviewTextArea').value;
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

    }
    function dislikeReview(userID, placeID, reviewID) {

    }