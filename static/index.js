let counter = 0;
let socket = null;
document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        // Create new message
        document.querySelector('#chat_box').onsubmit = () => {
            chat_text = document.querySelector('#chat_input').value;
            chat_room = document.querySelector('#chat_window').dataset.room_id;

            console.log(chat_text,chat_room);
            socket.emit('submit chat', {'chat_text':chat_text})
            document.querySelector('#chat_input').value = "";
            return false;
        }

        // Create new chat room
        document.querySelector('#room_form').onsubmit = () =>{
            room_name = document.querySelector('#room_input').value;
            socket.emit('submit new_room', {'room_name':room_name})
            document.querySelector('#room_input').value = ""
            return false;
        }
    })

    socket.on('announce chat', data => {
        // Test to see if announcement is in user chat room
        const chat_window = document.querySelector('#chat_window')
        let test_value = chat_window.dataset.room_id
        // console.log('current room:', test_value, 'emit room:',data.chat_room, (test_value == data.chat_room))
        // if announcemnet in current room add it to ul
        if (test_value == data.chat_room){
            const li = document.createElement('li')
            const ul = document.querySelector('#chat_window_list')
            li.innerHTML = '<strong>'+ data['user_name']+'</strong> ' + data['chat_text']
            // adjust scroll position if user has scrolled to bottom
            if(ul.clientHeight + ul.scrollTop >= ul.scrollHeight){
                ul.appendChild(li)
                li.scrollIntoView()
            } else{
                ul.appendChild(li)
            }
        }      
    })
    // When user changes room... update main chat window with message list
    socket.on('update room', data => {
        const ul = document.querySelector('#chat_window_list')
        for (var i=0; i< data.chat_log.length;i++){
            const li = document.createElement('li');
            li.innerHTML = data.chat_log[i].user_name + ": " + data.chat_log[i].text;
            ul.appendChild(li);
            li.scrollIntoView();
        }
    })  
    // Create new chat room

    // Listen for new chat room
})

function submit_chat(x){
    chat_text = document.querySelector('#chat_input').value
    console.log(chat_text)
    chat_room = 0
    x.emit('submit chat', {'chat_room':chat_room,'chat_text':chat_text})
    return false;
}
// Called when user clicks on new room
function change_room(key, value){
    const ul = document.querySelector('#chat_window_list')
    const chat_window = document.querySelector('#chat_window')
    // prepare data to be emitted
    let room_destination = key;
    let room_source = chat_window.dataset.room_id;
    let data = {"room_source":room_source,"room_destination":room_destination}
    console.log(`Room change. Source: ${room_source} -> Dest: ${room_destination}`)

    // Clear messages from message window and update message header
    chat_window.dataset.room_id = key
    while (ul.firstChild){
        ul.removeChild(ul.firstChild);
    const header = document.querySelector('#room_header')
    header.innerHTML = `Room: ${value['name']}`
    }
    socket.emit('submit room_change', data)   
}
