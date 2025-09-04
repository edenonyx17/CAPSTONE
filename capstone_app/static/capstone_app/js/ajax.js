// AJAX script for toggling task status without page reload

// Function to get CSRF token from cookies (standard Django practice)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    // Attach event listeners to all toggle buttons
    document.querySelectorAll('.toggle-status').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();  // Prevent default link behavior
            const url = this.href;  // Get the toggle URL
            const statusElement = this.closest('tr').querySelector('.task-status');  // Find status cell
            const toggleButton = this;  // Reference to the button

            // Send AJAX GET request
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',  // Mark as AJAX
                    'X-CSRFToken': getCookie('csrftoken')  // Get CSRF from cookie
                }
            })
            .then(response => response.json())  // Parse JSON response
            .then(data => {
                // Update status text (capitalize first letter)
                statusElement.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
                // Update button text
                toggleButton.textContent = data.status === 'pending' ? 'Mark Completed' : 'Mark Pending';
                // Remove overdue highlight if completed
                if (data.status === 'completed') {
                    statusElement.closest('tr').classList.remove('table-danger');
                }
            })
            .catch(error => console.error('Error:', error));  // Log errors
        });
    });
});