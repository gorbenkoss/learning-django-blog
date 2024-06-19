document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;
    const container = document.getElementById('posts-container');
    const username = container.getAttribute('data-username'); // Get the username from the data attribute

    
    function nearBottomOfPage() {
        return window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    }
    
    function loadMorePosts() {
        let url = `/blog/ajax/load_more_posts/?page=${currentPage}`;
        if (username) {
            url += `&username=${username}`;
        }
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.posts && data.posts.length > 0) {
                    appendPosts(data.posts);
                    currentPage++;
                    if (!data.has_next) {
                        window.removeEventListener('scroll', handleScroll); // No more posts
                    } else {
                        // After appending posts, check if the page still needs more posts to fill the screen
                        if (nearBottomOfPage()) {
                            loadMorePosts();
                        }
                    }
                }
            })
            .catch(err => console.error('Error loading more posts:', err));
    }

    function appendPosts(posts) {
        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post list-group-item';
            let editButtonHTML = post.can_edit ? `<a href="/blog/post/${post.id}/edit/" class="btn btn-warning">Edit</a>` : '';
            let buttonsHTML = `
                <button class="btn btn-success" onclick="sendReaction(${post.id}, 'post', true)">Like</button>
                <button class="btn btn-danger" onclick="sendReaction(${post.id}, 'post', false)">Dislike</button>
            `;
            let ratingDisplay = post.rating !== undefined ? post.rating : 0;
            postElement.innerHTML = `
                <h2><a href="/blog/post/${post.id}/">${post.title}</a></h2>
                <p>${post.content}</p>
                <p><small>Posted: ${formatDate(post.date_posted)}</small></p>
                <p><small>Posted by: <a href="/blog/account/${post.author}/">${post.author}</a></small></p>
                <p id="rating-post-${post.id}">${ratingDisplay}</p>
                <p><a href="/blog/post/${post.id}/">${post.comments_count} comments</a></p>
                ${buttonsHTML}
                ${editButtonHTML}
            `;
            container.appendChild(postElement);
        });
    }

    function handleScroll() {
        if (nearBottomOfPage()) {
            loadMorePosts();
        }
    }

    window.addEventListener('scroll', handleScroll);

    // Initial load
    loadMorePosts();
});
