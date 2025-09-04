// For reminders, notifications, and keyboard shortcuts

// Function to get cookie (for CSRF if needed elsewhere)
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

// Reminders and Notifications
function checkReminders() {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const dueCell = row.querySelector('td:nth-child(4)');
        if (dueCell && dueCell.textContent !== 'None') {
            const dueDateStr = dueCell.textContent;
            const dueDate = new Date(dueDateStr);
            const now = new Date();
            if (dueDate > now) {
                const timeDiff = dueDate - now;
                setTimeout(() => {
                    const title = row.querySelector('td:nth-child(1)').textContent;
                    if (Notification.permission === 'granted') {
                        new Notification('Task Due Reminder', { body: `Your task "${title}" is due now!` });
                    } else if (Notification.permission !== 'denied') {
                        Notification.requestPermission().then(permission => {
                            if (permission === 'granted') {
                                new Notification('Task Due Reminder', { body: `Your task "${title}" is due now!` });
                            } else {
                                alert(`Task Due: ${title}`);
                            }
                        });
                    } else {
                        alert(`Task Due: ${title}`);
                    }
                }, timeDiff);
            }
        }
    });
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        window.location.href = '/tasks/create/';
    } else if (e.shiftKey && e.key === 'D') {
        e.preventDefault();
        // Mark first pending task as done (simple implementation)
        const firstPending = document.querySelector('tr .task-status[textContent="Pending"] ~ td .toggle-status');
        if (firstPending) {
            firstPending.click();
        } else {
            alert('No pending tasks to mark as done.');
        }
    }
});

// Run on load
window.addEventListener('load', checkReminders);