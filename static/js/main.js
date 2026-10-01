document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');
    const sidebar = document.querySelector('.sidebar');
    const flashAlerts = document.querySelectorAll('.flash-alert');
    const closeButtons = document.querySelectorAll('.btn-close');

    if (navToggle && sidebar) {
        navToggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });
    }

    flashAlerts.forEach(function (alertBox) {
        alertBox.setAttribute('role', 'alert');
    });

    closeButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const alertElement = button.closest('.flash-alert');
            if (alertElement) {
                alertElement.remove();
            }
        });
    });
});
