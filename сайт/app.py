
from http.server import HTTPServer, BaseHTTPRequestHandler

HTML = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Аккаунт под защитой</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #080d20, #142849, #102f4b);
    color: white;
    min-height: 100vh;
    padding: 30px 15px;
}

.container {
    max-width: 780px;
    margin: auto;
}

header {
    text-align: center;
    margin-bottom: 30px;
}

.logo {
    font-size: 65px;
    margin-bottom: 12px;
}

h1 {
    font-size: 36px;
    color: #50dcff;
    margin-bottom: 12px;
}

.subtitle {
    color: #b9cce5;
    line-height: 1.6;
}

.card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.3);
}

.warning {
    background: rgba(255,190,60,0.1);
    border: 1px solid rgba(255,190,60,0.4);
    color: #ffda91;
    padding: 15px;
    border-radius: 12px;
    line-height: 1.5;
    margin-bottom: 22px;
    font-size: 14px;
}

.info {
    display: flex;
    justify-content: space-between;
    color: #a9c7e8;
    margin-bottom: 15px;
    font-size: 14px;
}

.progress {
    height: 9px;
    background: #263d60;
    border-radius: 20px;
    margin-bottom: 27px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    width: 0;
    background: linear-gradient(90deg, #36d9ff, #8374ff);
    transition: 0.4s;
}

.category {
    color: #5de5ff;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 13px;
}

.question {
    font-size: 23px;
    line-height: 1.45;
    margin-bottom: 25px;
}

.answers {
    display: grid;
    gap: 12px;
}

.answer {
    width: 100%;
    padding: 17px;
    border-radius: 12px;
    border: 2px solid #385578;
    background: #172e50;
    color: white;
    text-align: left;
    font-size: 16px;
    cursor: pointer;
    transition: 0.2s;
}

.answer:hover:not(:disabled) {
    border-color: #50dcff;
    background: #23466d;
    transform: translateY(-2px);
}

.answer:disabled {
    cursor: default;
}

.answer.selected {
    border-color: #4de4a0;
    background: #12533f;
}

.feedback {
    display: none;
    margin-top: 20px;
    padding: 17px;
    border-radius: 12px;
    background: #172f4b;
    border: 1px solid #42678e;
    line-height: 1.6;
    color: #d4e7ff;
}

.next, .restart {
    width: 100%;
    margin-top: 22px;
    padding: 17px;
    background: linear-gradient(90deg, #12bde8, #6868ff);
    border: none;
    border-radius: 12px;
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

.next {
    display: none;
}

.next:hover, .restart:hover {
    opacity: 0.85;
}

.result {
    display: none;
    text-align: center;
}

.result-icon {
    font-size: 75px;
    margin: 20px;
}

.score {
    font-size: 65px;
    font-weight: bold;
    color: #56e5ff;
    margin: 15px;
}

.level {
    font-size: 25px;
    margin: 15px;
}

.result-text {
    color: #c1d5ef;
    line-height: 1.7;
    margin: 20px 0;
}

.recommendations {
    text-align: left;
    background: #172e50;
    padding: 22px;
    border-radius: 15px;
    margin-top: 20px;
    line-height: 1.8;
}

.recommendations h3 {
    color: #5de5ff;
    margin-bottom: 12px;
}

footer {
    text-align: center;
    color: #829bb9;
    margin-top: 25px;
    font-size: 13px;
    line-height: 1.7;
}

@media(max-width: 500px) {
    h1 { font-size: 28px; }
    .card { padding: 20px; }
    .question { font-size: 20px; }
}
</style>
</head>

<body>

<div class="container">

<header>
    <div class="logo">🔐</div>
    <h1>АККАУНТ ПОД ЗАЩИТОЙ</h1>
    <p class="subtitle">
        Насколько защищён личный аккаунт обычного подростка?<br>
        Пройди тест и узнай, насколько безопасно ты пользуешься интернетом.
    </p>
</header>

<div class="card">

<div class="warning">
    ⚠️ Важно! Тест не просит вводить настоящие пароли,
    логины, номера телефонов или другие личные данные.
    Отвечай только о своих привычках.
</div>

<div id="quiz">

    <div class="info">
        <span id="number">Вопрос 1 из 10</span>
        <span id="points">Баллы: 0</span>
    </div>

    <div class="progress">
        <div class="progress-bar" id="progress"></div>
    </div>

    <div class="category" id="category"></div>

    <h2 class="question" id="question"></h2>

    <div class="answers" id="answers"></div>

    <div class="feedback" id="feedback"></div>

    <button class="next" id="next" onclick="nextQuestion()">
        Следующий вопрос →
    </button>

</div>

<div class="result" id="result">

    <div class="result-icon" id="resultIcon">🛡️</div>

    <h2>Проверка завершена!</h2>

    <div class="score" id="score">0%</div>

    <div class="level" id="level"></div>

    <p class="result-text" id="resultText"></p>

    <div class="recommendations">
        <h3>💡 Твои рекомендации:</h3>
        <div id="tips"></div>
    </div>

    <button class="restart" onclick="restartQuiz()">
        🔄 Пройти тест заново
    </button>

</div>

</div>

<footer>
    🔐 АККАУНТ ПОД ЗАЩИТОЙ<br>
    Твоя безопасность начинается с твоих привычек!
</footer>

</div>

<script>

const questions = [

{
category: "Пароли",
q: "Какой пароль ты обычно используешь для своих аккаунтов?",
a: [
"Один и тот же простой пароль везде",
"Разные пароли, но короткие и легко угадываемые",
"Длинные и уникальные пароли для разных аккаунтов"
],
points: [0, 1, 2],
tip: "Создавай длинные уникальные пароли. Можно использовать менеджер паролей."
},

{
category: "Двухфакторная защита",
q: "Включена ли у тебя двухфакторная аутентификация (2FA)?",
a: [
"Нет, я даже не знаю, что это",
"Включена только на некоторых аккаунтах",
"Да, на всех важных аккаунтах, где доступна"
],
points: [0, 1, 2],
tip: "Включи двухфакторную аутентификацию. Она добавляет дополнительную защиту при входе."
},

{
category: "Личные данные",
q: "Какие личные данные доступны незнакомым людям в твоём профиле?",
a: [
"Адрес, номер телефона или другие личные сведения",
"Некоторые личные сведения",
"Практически никакие личные данные"
],
points: [0, 1, 2],
tip: "Убери из открытого профиля номер телефона, домашний адрес и другие конфиденциальные сведения."
},

{
category: "Приватность",
q: "Какие настройки приватности установлены в твоих социальных сетях?",
a: [
"Профиль полностью открыт для всех",
"Некоторые публикации доступны только друзьям",
"Я проверил настройки и ограничил доступ к личной информации"
],
points: [0, 1, 2],
tip: "Проверь, кто может видеть твои публикации, фотографии, истории и личную информацию."
},

{
category: "Подозрительные ссылки",
q: "Что ты делаешь, если получаешь подозрительную ссылку?",
a: [
"Открываю её, если сообщение выглядит интересным",
"Сначала проверяю, кто её отправил",
"Не открываю подозрительные ссылки и проверяю их источник"
],
points: [0, 1, 2],
tip: "Не переходи по сомнительным ссылкам и никогда не вводи пароль на подозрительных сайтах."
},

{
category: "Устройства",
q: "Проверяешь ли ты, с каких устройств выполнен вход в твой аккаунт?",
a: [
"Никогда не проверяю",
"Проверял один раз",
"Регулярно проверяю активные сеансы и незнакомые устройства"
],
points: [0, 1, 2],
tip: "Периодически проверяй активные сеансы. Завершай неизвестные сеансы и меняй пароль, если подозреваешь взлом."
},

{
category: "Восстановление доступа",
q: "Насколько защищена электронная почта, привязанная к твоему аккаунту?",
a: [
"У неё простой пароль или нет дополнительной защиты",
"Есть отдельный пароль, но настройки восстановления не проверены",
"Есть уникальный пароль, 2FA и актуальные способы восстановления"
],
points: [0, 1, 2],
tip: "Защити электронную почту: она часто используется для восстановления доступа к другим аккаунтам."
},

{
category: "Общественные сети",
q: "Заходишь ли ты в личный аккаунт с чужих компьютеров или устройств?",
a: [
"Да, часто и не выхожу из аккаунта",
"Иногда, но стараюсь выходить после использования",
"Стараюсь не использовать чужие устройства для входа"
],
points: [0, 1, 2],
tip: "Не сохраняй пароли на чужих устройствах. Всегда выходи из аккаунта после использования."
},

{
category: "Защита от мошенников",
q: "Что ты сделаешь, если кто-то попросит прислать код из SMS или приложения?",
a: [
"Отправлю, если человек представится сотрудником поддержки",
"Сначала спрошу, зачем ему код",
"Не отправлю код никому"
],
points: [0, 1, 2],
tip: "Никому не сообщай коды подтверждения. Настоящие сотрудники поддержки не должны просить их у тебя."
},

{
category: "Обновления и безопасность",
q: "Следишь ли ты за обновлениями приложений и безопасностью своего устройства?",
a: [
"Нет, обновления обычно игнорирую",
"Обновляю приложения время от времени",
"Регулярно устанавливаю обновления и использую блокировку устройства"
],
points: [0, 1, 2],
tip: "Обновляй приложения и операционную систему. Используй надёжный PIN-код или биометрическую защиту устройства."
}

];

let current = 0;
let score = 0;
let answered = false;
let recommendations = [];

function loadQuestion() {

    answered = false;

    const q = questions[current];

    document.getElementById("number").textContent =
        `Вопрос ${current + 1} из ${questions.length}`;

    document.getElementById("points").textContent =
        `Баллы: ${score}`;

    document.getElementById("category").textContent =
        q.category;

    document.getElementById("question").textContent = q.q;

    document.getElementById("progress").style.width =
        (current / questions.length * 100) + "%";

    document.getElementById("feedback").style.display = "none";
    document.getElementById("next").style.display = "none";

    const answers = document.getElementById("answers");
    answers.innerHTML = "";

    q.a.forEach((answer, index) => {

        const button = document.createElement("button");

        button.className = "answer";
        button.textContent =
            String.fromCharCode(65 + index) + ". " + answer;

        button.onclick = () => checkAnswer(index);

        answers.appendChild(button);

    });

}

function checkAnswer(index) {

    if (answered) return;

    answered = true;

    const q = questions[current];
    const buttons = document.querySelectorAll(".answer");

    const earned = q.points[index];

    score += earned;

    buttons.forEach((button, i) => {

        button.disabled = true;

        if (i === index) {
            button.classList.add("selected");
        }

    });

    const feedback = document.getElementById("feedback");

    if (earned === 2) {

        feedback.innerHTML =
            "✅ <b>Отлично!</b><br>Ты выбрал безопасный вариант.";

    } else if (earned === 1) {

        feedback.innerHTML =
            "🟡 <b>Есть над чем поработать.</b><br>Твой вариант частично безопасен.";

        recommendations.push(q.tip);

    } else {

        feedback.innerHTML =
            "🔴 <b>Обрати внимание!</b><br>Этот вариант может поставить твой аккаунт под угрозу.";

        recommendations.push(q.tip);

    }

    feedback.innerHTML += "<br><br>💡 " + q.tip;

    feedback.style.display = "block";

    document.getElementById("points").textContent =
        `Баллы: ${score}`;

    const next = document.getElementById("next");
    next.style.display = "block";

    next.textContent =
        current === questions.length - 1
        ? "Узнать уровень защиты 🛡️"
        : "Следующий вопрос →";

}

function nextQuestion() {

    current++;

    if (current < questions.length) {
        loadQuestion();
    } else {
        showResult();
    }

}

function showResult() {

    document.getElementById("quiz").style.display = "none";
    document.getElementById("result").style.display = "block";

    const percent = Math.round(score / 20 * 100);

    document.getElementById("score").textContent =
        percent + "%";

    let level, icon, message;

    if (percent >= 85) {

        level = "🟢 Высокий уровень защиты";
        icon = "🏆";

        message = "Отличный результат! У тебя хорошие привычки цифровой безопасности. Продолжай следить за настройками аккаунта.";

    } else if (percent >= 55) {

        level = "🟡 Средний уровень защиты";
        icon = "🛡️";

        message = "Твой аккаунт защищён не полностью. Некоторые настройки и привычки стоит улучшить.";

    } else {

        level = "🔴 Низкий уровень защиты";
        icon = "⚠️";

        message = "Твой аккаунт может быть уязвим для мошенников и злоумышленников. Рекомендуем как можно скорее улучшить его защиту.";

    }

    document.getElementById("level").textContent = level;
    document.getElementById("resultIcon").textContent = icon;
    document.getElementById("resultText").textContent = message;

    const tips = document.getElementById("tips");

    if (recommendations.length === 0) {

        tips.innerHTML =
            "🎉 Отлично! Все твои ответы соответствуют безопасным привычкам. Продолжай в том же духе!";

    } else {

        tips.innerHTML = recommendations
            .map((tip, i) => `${i + 1}. ${tip}`)
            .join("<br><br>");

    }

}

function restartQuiz() {

    current = 0;
    score = 0;
    recommendations = [];

    document.getElementById("result").style.display = "none";
    document.getElementById("quiz").style.display = "block";

    loadQuestion();

}

loadQuestion();

</script>

</body>
</html>
"""


from flask import Flask, Response
import os

app = Flask(__name__)

@app.route("/")
def home():
    return Response(HTML, content_type="text/html; charset=utf-8")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
