document.addEventListener("DOMContentLoaded", function () {
//    restoreScrollPosition();
    makeTableRowsClickable();
    setupLikeHandlers();
    setupChangeStatusHandler();
    setupAddToCartHandler();
    checkTerms();
});

// Восстановление позиции прокрутки
function restoreScrollPosition() {
    const scrollPos = sessionStorage.getItem('scrollPos');
    if (scrollPos !== null) {
        window.scrollTo(0, parseInt(scrollPos, 10));
        sessionStorage.removeItem('scrollPos');
    }
}
window.onbeforeunload = () => sessionStorage.setItem('scrollPos', window.scrollY);

// Делает строки таблицы ссылками
function makeTableRowsClickable() {
    document.querySelectorAll(".clickable-row").forEach(row => {
        row.addEventListener("click", function () {
            window.location = this.dataset.href;
        });
    });
}

// Общий метод для отправки POST-запросов
function sendPostRequest(url, data = {}) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json());
}

// Получение CSRF-токена
function getCSRFToken() {
    let cookies = document.cookie.split(";").map(cookie => cookie.trim());
    for (let cookie of cookies) {
        if (cookie.startsWith("csrftoken=")) {
            return cookie.substring("csrftoken=".length);
        }
    }
    return "";
}

// Настроить лайки
function setupLikeHandlers() {
    document.querySelectorAll("a.like").forEach(likeButton => {
        likeButton.addEventListener("click", function (e) {
            e.preventDefault();
            sendPostRequest(this.dataset.url, { pk: this.dataset.pk, action: this.dataset.action })
                .then(data => {
                    if (data.status === "ok") {
                        toggleLikeState(likeButton, data);
                    }
                })
                .catch(error => console.error("Ошибка:", error));
        });
    });
}

// Переключает состояние лайка
function toggleLikeState(button, data) {
    let action = button.dataset.action === "like" ? "unlike" : "like";
    button.dataset.action = action;
    button.innerHTML = action === "like" ? '<i class="fas fa-heart-o"></i>' : '<i class="fas fa-heart"></i>';

    let likeCounter = document.querySelector(`.count_like_${button.dataset.pk}`);
    likeCounter.textContent = ` ${parseInt(likeCounter.textContent) + (action === "like" ? -1 : 1)}`;
}

// Настройка изменения статуса адресов
function setupChangeStatusHandler() {
    document.getElementById("tableAddress")?.addEventListener("click", function (event) {
        if (event.target.classList.contains("change-status")) {
            event.preventDefault();
            let button = event.target;
            sendPostRequest(button.dataset.url)
                .then(data => {
                    if (data.success) {
                        showMessage(data.message, data.message_type || "success");
                        updateStatusUI(data.active_address);
                    }
                })
                .catch(() => showMessage("Ошибка изменения статуса", "danger"));
        }
    });
}

// Обновляет UI статусов адресов
function updateStatusUI(activeAddressId) {
    document.querySelectorAll(".address-status").forEach(element => {
        let addressId = parseInt(element.dataset.addressId);
        element.innerHTML = addressId === activeAddressId
            ? `<b class="text-success">Основной</b>`
            : `<a href="#" class="change-status text-secondary" data-id="${addressId}" data-url="${element.dataset.statusUrl}">Неактивен</a>`;
    });
}

// Универсальная функция для вывода сообщений
function showMessage(message, type = "success") {
    let messageElement = document.getElementById("status-messages");
    messageElement.className = `alert alert-${type}`;
    messageElement.textContent = message;
    messageElement.style.display = "block";
    setTimeout(() => (messageElement.style.display = "none"), 3000);
}

// Настройка добавления в корзину
function setupAddToCartHandler() {
    document.querySelectorAll(".ajax-cart-add").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            sendPostRequest(this.dataset.url, { quantity: 1 })
                .then(data => {
                    if (data.success) {
                            updateCartUI();
                            updateCartPopup();
                            showMessage(data.message, data.status);}
                        else {
                            showMessage("Ошибка добавления в корзину", "danger");
                        }
                })
                .catch(() => showMessage("Ошибка выполнения запроса", "danger"));
        });
    });
}

// Обновление информации о корзине
function updateCartUI() {
    let cartElement = document.querySelector(".cart-counter");
    if (!cartElement) return;

    fetch(cartElement.dataset.url)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.cart_length>0){
                cartElement.innerHTML = `${data.cart_length}`;
                cartElement.style.visibility = "visible";}
                else{
                cartElement.innerHTML = ``;
                cartElement.style.visibility = "hidden";}
            }
        })
        .catch(() => console.error("Ошибка при обновлении количества в корзине"));
}

function updateCartPopup() {
    let cartContainer = document.querySelector(".box-popup-cart");
    if (!cartContainer) return;

    fetch(cartContainer.dataset.url)
        .then(response => response.text())  // Получаем HTML-код
        .then(html => {
                cartContainer.innerHTML = html;  // Заменяем содержимое всплывающего окна
        })
        .catch(error => console.error("Ошибка обновления popup окна корзины:", error));
}

function updatePreviewPopup(data) {
    let cartContainer = document.querySelector(".box-popup-preview");
    if (!cartContainer) return;

    fetch(data.url)
        .then(response => {
            // Логируем статус ответа
            console.log("Response status:", response.status);
            return response.text();  // Получаем HTML-код
        })  // Получаем HTML-код
        .then(html => {
            cartContainer.innerHTML = html;
            // Из за асинхронности fetch перенес из main сюда
            $(".box-popup-preview").show();
            initSlidePreview();
            setupAddToCartHandler();
        })
        .catch(error => console.error("Ошибка обновления popup preview:", error));
}

    // Показать комменты
function showReplyForm(commentId) {
    var form = document.getElementById("reply-form-" + commentId);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
    }

function checkTerms() {
    const checkbox = document.getElementById('termsCheckbox');
    const button = document.getElementById('placeOrderButton');
    if (!checkbox) return;

    checkbox.checked = false;
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            button.classList.remove('btn-disabled');
        } else {
            button.classList.add('btn-disabled');
        }
    });
}