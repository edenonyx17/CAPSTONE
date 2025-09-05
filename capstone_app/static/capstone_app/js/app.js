// For reminders, notifications, and keyboard shortcuts

// Function to get cookie (for CSRF if needed elsewhere)
function checkReminders() {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const statusCell = row.querySelector('.task-status');
        const dueCell = row.querySelector('td:nth-child(5)');  // Adjust index if needed
        const titleCell = row.querySelector('td:nth-child(1)');
        const taskPk = row.getAttribute('data-task-pk');

        if (statusCell && statusCell.textContent.trim() === 'Pending' && dueCell && dueCell.textContent.trim() !== 'None') {
            const dueDateStr = dueCell.textContent.trim();
            const dueDate = new Date(dueDateStr);
            const now = new Date();

            if (isNaN(dueDate.getTime())) {
                console.error(`Invalid due date for task "${titleCell.textContent.trim()}": ${dueDateStr}`);
                return;
            }

            const timeDiff = dueDate - now;
            const title = titleCell.textContent.trim();

            if (timeDiff <= 0) {
                notifyUser(title, '⚠️ Your task is overdue!', taskPk);
            } else {
                setTimeout(() => {
                    notifyUser(title, '⏰ Your task is due now!', taskPk);
                }, timeDiff);
            }
        }
    });
}


// Helper to send notification or alert
function notifyUser(title, message, taskPk) {
    if (Notification.permission === 'granted') {
        const notification = new Notification('Task Reminder', { body: `${message} - ${title}` });
        notification.onclick = function () {
            window.open(`/tasks/${taskPk}/update/`, '_blank');
        };
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                const notification = new Notification('Task Reminder', { body: `${message} - ${title}` });
                notification.onclick = function () {
                    window.open(`/tasks/${taskPk}/update/`, '_blank');
                };
            } else {
                alert(`${message} - ${title}`);
            }
        });
    } else {
        alert(`${message} - ${title}`);
    }
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
            firstPending.click();  // Simulate click on toggle
        } else {
            alert('No pending tasks to mark as done.');
        }
    }
});

// Run on load
window.addEventListener('load', () => {
    // Request permission early
    if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
        Notification.requestPermission();
    }
    checkReminders();
});