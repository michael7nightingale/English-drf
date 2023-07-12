document.querySelector('#username-input').focus();
        document.querySelector('#username-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#submit-button').click();
            }
        };

        document.querySelector('#submit-button').onclick = getJWTToken(event)


async function getJWTToken(event){
            console.log(12`3123123123`);
    let username = document.querySelector("#username-input").value;
    let password = document.querySelector('#password-input').value;

    let data = {
        username: username,
        password: password
    }

    let response = await fetch("http://localhost:8000/api/v1/auth/token/",
        {method: "POST", body: JSON.stringify(data)}
    )
    console.log(response.json());


    window.location.pathname = '/api/v1/chats/room-html/';
}

