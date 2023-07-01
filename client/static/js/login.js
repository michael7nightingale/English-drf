async function logIn(event){
    let loginName = document.getElementById("loginName").value;
    let password = document.getElementById("loginName").value;
    let data = {"username": loginName, "password": password};
    let response = await fetch(
        "https://localhost:8000/api/v1/auth/token/",
         {
          method: "POST", // or 'PUT'
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
    );
    console.log(response);
    const jsonData = await response.json();
    if (response.status != 200) {
        alert(jsonData.detail);
    }
    else{
        window.location.replace("index.html")
    }
}

