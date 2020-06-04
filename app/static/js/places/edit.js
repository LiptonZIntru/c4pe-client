function deleteThis(place_id, string) {
    if (confirm('Do you really want to delete this image?')) {
        window.location = '/places/' + place_id + '/images/' + string + '/delete/';
    }
}

/* File upload control */
    $(".custom-file-input").on("change", function() {
      var fileName = $(this).val().split("\\").pop();
      $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });