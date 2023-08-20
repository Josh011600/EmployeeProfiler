document.addEventListener('DOMContentLoaded', function () {
    const showAllButton = document.getElementById('show-all');
    const showIncompleteButton = document.getElementById('show-incomplete');
    const showCompleteButton = document.getElementById('show-complete');
    const taskTable = document.getElementById('task-table');

    showAllButton.addEventListener('click', function () {
        taskTable.style.display = 'table';
    });

    showIncompleteButton.addEventListener('click', function () {
        hideCompletedTasks();
        taskTable.style.display = 'table';
    });

    showCompleteButton.addEventListener('click', function () {
        hideIncompleteTasks();
        taskTable.style.display = 'table';
    });

    function hideCompletedTasks() {
        // Code to hide completed tasks in the table
    }

    function hideIncompleteTasks() {
        // Code to hide incomplete tasks in the table
    }
});
