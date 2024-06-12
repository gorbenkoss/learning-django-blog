function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function sendReaction(postId, isLike) {
    var csrftoken = $('meta[name="csrf-token"]').attr('content');
    
    $.ajax({
        url: `/blog/${isLike ? 'like' : 'dislike'}/${postId}/`,
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        success: function(response) {
            console.log('Success:', response);
            updateRatingDisplay(postId, response.rating);
        },
        error: function(xhr, status, error) {
                console.error('Failed:', status, error);
            }
    });
}

function updateRatingDisplay(postId, newRating) {
    const ratingElement = document.getElementById(`rating-${postId}`);
    if (ratingElement) {
        ratingElement.textContent = `Rating: ${newRating}`;
    }
}