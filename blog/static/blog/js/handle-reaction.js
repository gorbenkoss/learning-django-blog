function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function sendReaction(contentId, contentType, isLike) {
    var csrftoken = $('meta[name="csrf-token"]').attr('content');
    
    $.ajax({
        url: `/blog/react/${contentType}/${contentId}/`,
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            liked:  isLike
        },
        success: function(response) {
            console.log('Success:', response);
            updateRatingDisplay(contentType, contentId, response.rating);
        },
        error: function(xhr, status, error) {
            console.error('Failed:', status, error);
        }
    });
}

function updateRatingDisplay(contentType, contentId, newRating) {
    const ratingElement = document.getElementById(`rating-${contentType}-${contentId}`);
    if (ratingElement) {
        ratingElement.textContent = `${newRating}`;
    }
}