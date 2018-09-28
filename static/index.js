let counter = 0;
document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        document.querySelector('button').onclick = count;
        // document.querySelector('#chat_box').onsubmit = submit_chat(socket);
        document.querySelector('#chat_box').onsubmit = () => {
            chat_text = document.querySelector('#chat_input').value;
            console.log(chat_text);
            chat_room = 0;
            socket.emit('submit chat', {'chat_room':chat_room,'chat_text':chat_text});
            document.querySelector('#chat_input').value = "";
            return false;
        }
    })

    socket.on('announce chat', data => {
        const li = document.createElement('li')
        const ul = document.querySelector('#chat_window_list')
        li.innerHTML = data['chat_text']
        
        if(ul.clientHeight+ul.scrollTop >= ul.scrollHeight){
            ul.appendChild(li)
            li.scrollIntoView()
        } else{
            ul.appendChild(li)
        }
        // document.querySelector('h1').innerHTML = data['chat_text']
    })

    
})

function count() {
    counter ++;
    document.querySelector('h1').innerHTML = counter;
}

function submit_chat(x){
    chat_text = document.querySelector('#chat_input').value
    console.log(chat_text)
    chat_room = 0
    x.emit('submit chat', {'chat_room':chat_room,'chat_text':chat_text})
    return false;
}