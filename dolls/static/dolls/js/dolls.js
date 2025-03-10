

    // Сохраняем позицию перед уходом
    window.onbeforeunload = () => {
        sessionStorage.setItem('scrollPos', window.scrollY);
    };

    // Восстанавливаем позицию после загрузки
    window.onload = () => {
        const scrollPos = sessionStorage.getItem('scrollPos');
        if (scrollPos) {
            window.scrollTo(0, scrollPos);
            sessionStorage.removeItem('scrollPos'); // Удаляем позицию после использования
        }
    };

    // Для лайков
    const csrftoken = Cookies.get('csrftoken');
    document.addEventListener('DOMContentLoaded', (event) => {
        // DOM загружена
        var options = {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin'
        }
        document.querySelectorAll('a.like').forEach(element => {
            element.addEventListener('click', function(e){
                e.preventDefault();
                var likeButton = this;
                // Добавить тело запроса
                var formData = new FormData();
                formData.append('pk', likeButton.dataset.pk);
                formData.append('action', likeButton.dataset.action);
                options['body'] = formData;
                // Отправить HTTP-запрос
                fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    if (data['status'] === 'ok') {
                        var previousAction = likeButton.dataset.action;
                        // Переключить текст кнопки и атрибут data-action
                        var action = previousAction === 'like' ? 'unlike' : 'like';
                        likeButton.dataset.action = action;
                        likeButton.innerHTML = previousAction === 'like' ? '<i class="fa fa-heart"></i>':'<i class="fa fa-heart-o"></i>';
                        // Обновить количество лайков
                        var likeCount = document.querySelector('span.count_like_' + likeButton.dataset.pk);
                        var totalLikes = parseInt(likeCount.innerHTML);
                        likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
                    }
                })
                .catch(error => console.error('Ошибка:', error));
            });
        });
    });