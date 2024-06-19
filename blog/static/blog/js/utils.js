// utils.js
function formatDate(date) {
    const postDate = new Date(date);
    const now = new Date();
    const diffMs = (now - postDate); // milliseconds between now & post date
    const diffDays = Math.floor(diffMs / 86400000); // days
    const diffHrs = Math.floor((diffMs % 86400000) / 3600000); // hours
    const diffMins = Math.round(((diffMs % 86400000) % 3600000) / 60000); // minutes

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
