/* ZABARVENI REVIEW NAVBAR TLACITKA A SCHOVAVANI / UKAZOVANI FILTROVANYCH RECENZI */
    function colorReviewNavBar(type) {
        var user_id = document.getElementById('user_id').value;
        var matches = false;
        var place_id = document.getElementById('place_id').value;
        $.get("/places/" + place_id + "/reviews/type/" + type, function(data) {
            var reviews = JSON.parse(data);
            if(type == 1) {
                reviews.forEach(review => {
                    if (review.user.id == user_id) {
                        matches = true; }
                })
            }
            else if (type == 2) {
                reviews.forEach(review => {
                    if (review.user.id == user_id && review.rating > 3) {
                        matches = true; }
                })
            }
            else if (type == 3) {
                reviews.forEach(review => {
                    if(review.user.id == user_id && review.rating < 4) {
                        matches = true; }
                })
            }
            else if (type == 4) {
                reviews.forEach(review => {
                    if(review.user.id == user_id && review.user.isVerified) {
                        matches = true; }
                })
            }
            document.getElementById('currentUserReview').hidden = !matches;
        })

        document.getElementById('all-link').classList = "nav-link text-primary";
        document.getElementById('positive-link').classList = "nav-link text-primary";
        document.getElementById('negative-link').classList = "nav-link text-primary";
        document.getElementById('verified-link').classList = "nav-link text-primary";

        document.getElementById('all-reviews').classList = "d-none";
        document.getElementById('positive-reviews').classList = "d-none";
        document.getElementById('negative-reviews').classList = "d-none";
        document.getElementById('verified-reviews').classList = "d-none";

        if (type == 1) {
            document.getElementById('all-link').classList = "nav-link active";
            document.getElementById('all-reviews').classList = "d-block";
        }
        else if (type == 2) {
            document.getElementById('positive-link').classList = "nav-link active";
            document.getElementById('positive-reviews').classList = "d-block";
        }
        else if (type == 3) {
            document.getElementById('negative-link').classList = "nav-link active";
            document.getElementById('negative-reviews').classList = "d-block";
        }
        else if (type == 4) {
            document.getElementById('verified-link').classList = "nav-link active";
            document.getElementById('verified-reviews').classList = "d-block";
        }
    }