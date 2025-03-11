window.onbeforeunload = () => { savePos(); };
window.onload = () => { restorePos(); };

function savePos() {
    // Сохраняем позицию прокрутки перед уходом
    sessionStorage.setItem('scrollPos', window.scrollY);
}

function restorePos() {
    // Восстанавливаем позицию прокрутки после загрузки
    const scrollPos = sessionStorage.getItem('scrollPos');

    if (scrollPos !== null) { // Проверяем, что значение существует
        window.scrollTo(0, parseInt(scrollPos, 10)); // Преобразуем в число
        sessionStorage.removeItem('scrollPos'); // Удаляем позицию после использования
    }
}

  // Строка в таблице ссылка
  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".clickable-row").forEach(row => {
      row.addEventListener("click", function() {
        window.location = this.dataset.href;
      });
    });
  });

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

    function showReplyForm(commentId) {
    var form = document.getElementById("reply-form-" + commentId);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
    }