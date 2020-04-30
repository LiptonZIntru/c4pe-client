var stars = ['oneStar', 'twoStar', 'threeStar', 'fourStar', 'fiveStar'];
var freezed = false;
var rating = 0;

function star(element) {
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
function save()
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
function updateText() {
    document.getElementById('text').value = document.getElementById('newReview').value;

}