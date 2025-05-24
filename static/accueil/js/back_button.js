document.addEventListener('DOMContentLoaded', function() {
    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.addEventListener('click', function(e) {
            e.preventDefault();
            const previousURL = localStorage.getItem('previousPageURL');
            if (previousURL) {
                window.location.href = previousURL;
            } else {
                window.history.back();
            }
        });
    }
});