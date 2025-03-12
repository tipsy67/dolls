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
    document.addEventListener('DOMContentLoaded', (event) => {
        // DOM загружена
        var options = {
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()},
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

    // Показать комменты
    function showReplyForm(commentId) {
    var form = document.getElementById("reply-form-" + commentId);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
    }


    // Смена статуса адресов
document.addEventListener("DOMContentLoaded", function () {
    // Делегирование событий на родительский элемент, содержащий все адреса
    // (лучше использовать id таблицы вместо класса отдельной строки)
    document.querySelector("table").addEventListener("click", function (event) {
        // Проверяем, был ли клик на элементе с классом change-status
        if (event.target.classList.contains("change-status")) {
            event.preventDefault();

            let button = event.target;
            let addressId = button.dataset.id; // Используем data-id как в HTML
            let changeStatusUrl = button.dataset.url;

            fetch(changeStatusUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Показываем сообщение пользователю
                    showMessage(data.message, data.message_type || 'success');
                    updateStatusUI(data.active_address);
                }
            })
            .catch(error => {
                console.error("Ошибка:", error);
                showMessage("Произошла ошибка при изменении статуса", "danger");
            });
        }
    });
});

// Function to update UI after changing status
function updateStatusUI(activeAddressId) {
    document.querySelectorAll(".address-status").forEach(element => {
        let addressId = parseInt(element.dataset.addressId);
        let statusUrl = element.dataset.statusUrl; // Используем предварительно сохраненный URL

        if (addressId === activeAddressId) {
            element.innerHTML = `<b>Основной</b>`;
        } else {
            element.innerHTML = `<a href="#" class="change-status" data-id="${addressId}" data-url="${statusUrl}">Неактивен</a>`;
        }
    });
}

// Функция отображения сообщения
function showMessage(message, type = 'success') {
    const messageElement = document.getElementById('status-messages');

    // Установка класса для стилизации (Bootstrap классы)
    messageElement.className = `alert alert-${type}`;
    messageElement.textContent = message;
    messageElement.style.display = 'block';

    // Автоматическое скрытие сообщения через 3 секунды
    setTimeout(() => {
        messageElement.style.display = 'none';
    }, 3000);
}

// Добавление в корзину
document.addEventListener('DOMContentLoaded', function() {
    const addToCartLinks = document.querySelectorAll('.ajax-cart-add');

    addToCartLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const productId = this.dataset.product_id;
            const url = this.dataset.url;

            const formData = new FormData();
            formData.append('quantity', 1);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                const cartCounter = document.querySelector('.cart-counter');
                if (cartCounter) {
                    cartCounter.textContent = data.cart_total;
                }
                updateCartUI();
                showMessage(data.message, data.status);
            })
            .catch(error => {
                showMessage('При добавлении в корзину произошла ошибка', 'error');
            });
        });
    });
 });

// Function to get CSRF token from cookie (for Django)
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}

//получим корзину
function getCartData(url) {
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                return data.cart_length; // Возвращаем объект с данными корзины
            } else {
                return null; // Если `success` ложное, возвращаем null
            }
        })
        .catch(error => {
            console.error("Ошибка при получении данных:", error);
            return null; // В случае ошибки возвращаем null
        });
}

function updateCartUI() {
    const element = document.getElementById("cart-count");
    if (!element) return; // Проверяем наличие элемента, чтобы избежать ошибок

    getCartData(element.dataset.url)
        .then(cartData => {
            if (cartData) {
                element.innerHTML = `<i class="icon icon-ShoppingCart"></i> ${cartData}`;
            }
        })
        .catch(error => {
            console.error("Ошибка при обновлении корзины:", error);
        });
}