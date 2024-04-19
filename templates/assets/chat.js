// Utils
const get = (selector, root = document) => root.querySelector(selector);

const formatDate = date =>
{
    const h = '0' + date.getHours();
    const m = '0' + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
};

const random = (min, max) => Math.floor(Math.random() * (max - min) + min);

const appendMessage = (domChat, fromName, img, position, text) =>
{
    const elHtml = `
    <div class="msg ${position}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${fromName}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

    domChat.insertAdjacentHTML('beforeend', elHtml);
    domChat.scrollTop += 500;
};

window.addEventListener('load', () =>
{
    const messengerFrom = get('.msger-inputarea');
    const messengerInputField = get('.msger-input');
    const messengerChatList = get('.msger-chat');

    const BOT_IMG = 'https://api.iconify.design/carbon:chat-bot.svg';
    const BOT_NAME = 'BOT';

    const PERSON_IMG = 'https://api.iconify.design/carbon:user-avatar.svg';
    const PERSON_NAME = 'You';

    const socket = new ReconnectingWebSocket('ws://127.0.0.1:8000/chats/123', [], {
        onopen: () =>
        {
            console.log('Connected');
            appendMessage(messengerChatList, BOT_NAME, BOT_IMG, 'left', 'Hi, and welcome to Random Chat! Go ahead and send me a message.');
        },
        onclose: () => console.log('Disconnected'),
        onmessage: (event) =>
        {
            console.log('Received message:', event.data);
            appendMessage(messengerChatList, BOT_NAME, BOT_IMG, 'left', event.data);
        },
        onerror: (error) => console.error('WebSocket error:', error),
        onmaximumreconnectattempts: () => console.error('Maximum reconnect attempts reached'),
        maxReconnectAttempts: 10,
        reconnectInterval: 2000,
        reconnectDecay: 2
    });

    messengerFrom.addEventListener('submit', event =>
    {
        event.preventDefault();

        const msgText = messengerInputField.value;
        if (!msgText)
        {
            return;
        }

        appendMessage(messengerChatList, PERSON_NAME, PERSON_IMG, 'right', msgText);
        messengerInputField.value = '';

        if (socket.readyState !== 1)
        {
            socket.send(msgText);
        }
    });
});
