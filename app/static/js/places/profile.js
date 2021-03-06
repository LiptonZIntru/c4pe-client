var newStars = ['oneStar', 'twoStar', 'threeStar', 'fourStar', 'fiveStar'];
var editStars = ['oneStarEdit', 'twoStarEdit', 'threeStarEdit', 'fourStarEdit', 'fiveStarEdit'];
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
        var place_id = document.getElementById('place_id').value;
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

/* VYKRESLUJE HVĚZDY PŘI PSANÍ RECENZE */
    function colorStars(element) {
        if(!freezed){
            if (element.id.includes('oneStar')) {
                rating = 1;
            } else if (element.id.includes('twoStar')) {
                rating = 2;
            } else if (element.id.includes('threeStar')) {
                rating = 3;
            } else if (element.id.includes('fourStar')){
                rating = 4;
            } else if (element.id.includes('fiveStar')) {
                rating = 5;
            }

            if(element.id.includes('Edit'))
                for (var i = 0; i < editStars.length; i++) {
                    if (i < rating) document.getElementById(editStars[i]).classList = "fa fa-star";
                    else document.getElementById(editStars[i]).classList = "fa fa-star-o";
                }
            else
            {
                for (var i = 0; i < newStars.length; i++) {
                    if(i < rating) document.getElementById(newStars[i]).classList = "fa fa-star";
                    else document.getElementById(newStars[i]).classList = "fa fa-star-o";
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
    function blueThis(parent, id, method)
    {
        if(!document.getElementById(parent).children[id].classList.contains('permanent')) {
            if(method == 'over') {
                document.getElementById(parent).children[id].classList.add('text-primary');
                document.getElementById(parent).children[id].classList.remove('text-secondary');
            }
            else {
                document.getElementById(parent).children[id].classList.add('text-secondary');
                document.getElementById(parent).children[id].classList.remove('text-primary');
            }
        }

    }

/* LIKE/DISLIKE RECENZE */
    function reviewReaction(parent, placeID, reviewID, elementID) {
        var likeDislikeButton = document.getElementById(parent).children[elementID];
        $.get('/places/' + placeID + '/reviews/' + reviewID + (elementID.includes('positive') ? '/like/' : '/dislike/'), function (data) {
            var reactions = JSON.parse(data);

            if (reactions.success.includes('liked'))
            {
                likeDislikeButton.classList.remove('text-secondary');
                likeDislikeButton.classList.add('text-primary', 'permanent');
            }
            else if (reactions.success == 'deleted')
            {
                likeDislikeButton.classList.remove('text-primary', 'permanent');
                likeDislikeButton.classList.add('text-secondary');
            }

            if(reactions.success == 'liked' && document.getElementById(parent).children['negativeReaction_' + reviewID].classList.contains('permanent')) {
                document.getElementById(parent).children['negativeReaction_' + reviewID].classList.remove('text-primary', 'permanent');
                document.getElementById(parent).children['negativeReaction_' + reviewID].classList.add('text-secondary');
            }
            else if (reactions.success == 'disliked' && document.getElementById(parent).children['positiveReaction_' + reviewID].classList.contains('permanent')) {
                document.getElementById(parent).children['positiveReaction_' + reviewID].classList.remove('text-primary', 'permanent');
                document.getElementById(parent).children['positiveReaction_' + reviewID].classList.add('text-secondary');
            }

            document.getElementById(parent).children['positiveReactionCount_' + reviewID].innerHTML = reactions.positiveReactions;
            document.getElementById(parent).children['negativeReactionCount_' + reviewID].innerHTML = reactions.negativeReactions;
        })
    }

/* EDITACE RECENZE */
    function editReview(revRat)
    {
        var editReviewButton = document.getElementById('editReviewButton');
        var submitReviewButton = document.getElementById('submitReviewButton');
        var reviewForm = document.getElementById('editReview');
        var reviewRating = document.getElementById('editReviewRating');
        var staticReview = document.getElementById('editReviewContent');
        var staticRating = document.getElementById('staticRating');

        rating = revRat;
        for (var i = 0; i < editStars.length; i++) {
            if(i < rating) document.getElementById(editStars[i]).classList = "fa fa-star";
            else document.getElementById(editStars[i]).classList = "fa fa-star-o";
        }

        if(!editReviewButton.hidden)
        {
            editReviewButton.hidden = true;
            reviewForm.hidden = false;
            reviewRating.hidden = false;
            staticReview.hidden = true;
            staticRating.hidden = true;
            submitReviewButton.hidden = false;
        }
        else
        {
            editReviewButton.hidden = false;
            reviewForm.hidden = true;
            reviewRating.hidden = true;
            staticReview.hidden = false;
            staticRating.hidden = false;
            submitReviewButton.hidden = true;
        }
        freezed = true;
    }

/* SMAZÁNÍ REVIEW */
    function deleteReview(review_id, place_id)
    {
        if(confirm("Do you really want to delete this review?")) {
            window.location = "/places/" + place_id + "/reviews/" + review_id + "/delete/";
        }
    }