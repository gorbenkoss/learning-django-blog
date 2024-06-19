document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;
    const commentsContainer = document.getElementById('comments-container');
    const postId = commentsContainer.getAttribute('data-post-id');
    const totalComments = commentsContainer.getAttribute('data-total-comments');

    function nearBottomOfPage() {
        return window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    }

    function loadMoreComments() {
        fetch(`/blog/post/${postId}/load-more-comments/?page=${currentPage}`)
            .then(response => response.json())
            .then(data => {
                if (data.comments && data.comments.length > 0) {
                    appendComments(data.comments);
                    currentPage++;
                    if (!data.has_next) {
                        window.removeEventListener('scroll', handleScroll); // No more comments
                    } else {
                        // After appending comments, check if the page still needs more comments to fill the screen
                        if (nearBottomOfPage()) {
                            loadMoreComments();
                        }
                    }
                }
            })
            .catch(err => console.error('Error loading more comments:', err))
    }

    function appendComments(comments) {
        comments.forEach(comment => {
            const commentElement = document.createElement('div');
            commentElement.className = 'comment list-group-item';
            let buttonsHTML = `
                <button class="btn btn-success" onclick="sendReaction(${comment.id}, 'comment', true)">Like</button>
                <button class="btn btn-danger" onclick="sendReaction(${comment.id}, 'comment', false)">Dislike</button>
        `;
            commentElement.innerHTML = `
                <p>${comment.content}</p>
                <p><small>Commented by: <a href="/blog/account/${comment.author}/">${comment.author}</a></small></p>
                <p><small>Commented on: ${formatDate(comment.date_posted)}</small></p>
                <p><small>${buttonsHTML} <p id=rating-comment-${comment.id}>${comment.rating}</p></small></p>
            `;
            commentsContainer.appendChild(commentElement);
        });
    }

    function handleScroll() {
        if (nearBottomOfPage() && currentPage * 2 < totalComments) {
            loadMoreComments();
        }
    }

    window.addEventListener('scroll', handleScroll);

    // Check if more comments are needed after the initial load
    if (nearBottomOfPage() && currentPage * 2 < totalComments) {
        loadMoreComments();
    }
    loadMoreComments()
});
