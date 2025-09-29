// static/autocomplete.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const autocompleteList = document.getElementById('autocomplete-list');

    searchInput.addEventListener('input', debounce(function(e) {
        const query = e.target.value.trim();

        // Очищаем список, если запрос пустой
        if (query.length < 2) {
            closeAutocompleteList();
            return;
        }

        // Выполняем запрос к API
        fetch(`/api/autocomplete?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(suggestions => {
                showAutocompleteSuggestions(suggestions);
            })
            .catch(error => {
                console.error('Ошибка при запросе автодополнения:', error);
            });
    }, 300)); // Задержка 300 мс для debounce

    function showAutocompleteSuggestions(items) {
        closeAutocompleteList();
        if (items.length === 0) return;

        autocompleteList.innerHTML = ''; // Очищаем старые предложения

        items.forEach(item => {
            const div = document.createElement('div');
            div.textContent = item;
            // При клике на подсказку вставляем её текст в поле ввода
            div.addEventListener('click', function() {
                searchInput.value = item;
                closeAutocompleteList();
                // Можно сразу отправить форму: searchInput.form.submit();
            });
            autocompleteList.appendChild(div);
        });
    }

    function closeAutocompleteList() {
        autocompleteList.innerHTML = '';
    }

    // Функция debounce для ограничения частоты запросов
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Закрываем выпадающий список при клике вне его
    document.addEventListener('click', function(e) {
        if (!autocompleteList.contains(e.target) && e.target !== searchInput) {
            closeAutocompleteList();
        }
    });
});