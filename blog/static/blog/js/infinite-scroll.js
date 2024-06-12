document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;
    const container = document.getElementById('posts-container');
    const username = container.getAttribute('data-username'); // Get the username from the data attribute


    function nearBottomOfPage() {
        return window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    }

    function formatDate(date) {
        const postDate = new Date(date);
        const now = new Date();
        const diffMs = (now - postDate);
        const diffDays = Math.floor(diffMs / 86400000);
        const diffHrs = Math.floor((diffMs % 86400000) / 3600000);
        const diffMins = Math.round(((diffMs % 86400000) % 3600000) / 60000);

        if (diffDays > 0) {
            return postDate.toLocaleDateString("en-US", { month: 'long', day: 'numeric', year: 'numeric' }) + ", " + postDate.toLocaleTimeString("en-US", { hour: 'numeric', minute: 'numeric', hour12: true });
        } else if (diffHrs > 0) {
            return `today, at ${postDate.toLocaleTimeString("en-US", { hour: 'numeric', minute: 'numeric', hour12: true })}`;
        } else if (diffMins > 0) {
            return `${diffMins} minutes ago`;
        } else {
            return "just now";
        }
    }

    function loadMorePosts() {
        const url = username ? `/blog/ajax/load_more_posts/?page=${currentPage}&username=${username}` : `/blog/ajax/load_more_posts/?page=${currentPage}`;
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.posts && data.posts.length > 0) {
                    appendPosts(data.posts);
                    currentPage++;
                    if (!data.has_next) {
                        window.removeEventListener('scroll', handleScroll); // No more posts
                    } else {
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
            postElement.className = 'post';
            let editButtonHTML = post.can_edit ? `<a href="/blog/post/${post.id}/edit/"><button>Edit</button></a>` : '';
            let buttonsHTML = `
                <button onclick="sendReaction(${post.id}, true)">Like</button>
                <button onclick="sendReaction(${post.id}, false)">Dislike</button>
            `;
            let ratingDisplay = post.rating !== undefined ? post.rating : 0;
            postElement.innerHTML = `
                <h2><a href="/blog/post/${post.id}/">${post.title}</a></h2>
                <p>${post.content}</p>
                <p><small>Posted: ${formatDate(post.date_posted)}</small></p>
                <p><small>Posted by: <a href="/blog/account/${post.author}/">${post.author}</a></small></p>
                <p id="rating-${post.id}">Rating: ${ratingDisplay}</p>
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

    // Load initial posts
    loadMorePosts();
});