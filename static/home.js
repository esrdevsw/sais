document.addEventListener('DOMContentLoaded', function () {
    const startChatButton = document.getElementById("startChat");
    const viewInteractionsButton = document.getElementById("viewInteractions");
    const logoutButton = document.getElementById('logoutButton');

    startChatButton.addEventListener("click", function () {
        window.open("/chat", "_blank");
    });

    if (viewInteractionsButton) {
        viewInteractionsButton.addEventListener("click", function () {
            window.open("/interactions", "_blank");
        });
    }

    logoutButton.addEventListener('click', function () {
        // Send a request to the server to clear the session
        fetch('/logout', {
            method: 'GET',
        })
        .then(response => {
            if (response.status === 200) {
                // Redirect to the login page
                window.location.href = '/logout';
            } else {
                // Handle any errors or unexpected behavior
                console.error('Error logging out');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
