// interactions.js

document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const removeButton = document.getElementById('removeButton');

    // Add a click event listener to the "Remove Selected" button
    removeButton.addEventListener('click', function () {
        const selectedIds = [];
        checkboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                selectedIds.push(checkbox.getAttribute('data-id'));
            }
        });

        if (selectedIds.length > 0) {
            if (window.confirm('Are you sure you want to remove the selected interactions?')) {
                // Send a request to the server to remove the selected interactions
                fetch('/remove_interactions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ selected_ids: selectedIds }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Handle successful removal if needed
                            console.log('Interactions removed successfully');
                            // Uncheck all checkboxes
                            checkboxes.forEach(function (checkbox) {
                                checkbox.checked = false;
                            });
                            // Reload the page after removal
                            location.reload();
                        } else {
                            // Handle removal failure if needed
                            console.error('Error:', data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        } else {
            alert('Please select interactions to remove.');
        }
    });
});
