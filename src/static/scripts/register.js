console.log("script is working")

const form = document.getElementById('auth-form');
const resultDiv = document.getElementById('result');
        
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Собираем данные с формы
    const userData = {
        nickname: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
    };
    
    try {
        // Отправляем POST запрос на бэкенд
        const response = await fetch('http://localhost:8000/api/v1/reg/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Отображаем результат
        resultDiv.innerHTML = `
            <h3>Ответ от сервера:</h3>
            <p><strong>Сообщение:</strong> ${result.msg}</p>
        `;

        console.log(result.msg)
        
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">Ошибка: ${error.message}</p>`;
        console.log(error.message)
    }
});