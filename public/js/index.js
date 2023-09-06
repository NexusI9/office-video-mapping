
function __main__(){
    
    //replace form values with config values
    fetch('/getConfig',{ method:'POST' })
        .then( resp => resp.json() )
        .then( data => {

            document.querySelectorAll('#updateform input').forEach( item => {
                Object.keys( data ).map( parentKey => {
                    Object.keys( data[parentKey] ).map( childKey => {
                        if(item.id.includes(`${parentKey}_${childKey}`)){
                            item.value = data[parentKey][childKey];
                        }
                    });
                });
            });
        } );
    

    //on submit post values to servers to update config.json
    document.querySelectorAll('form').forEach( item => {
        
        item.addEventListener("submit", function (e) {
            e.preventDefault(); // prevent page reload
            const url = item.getAttribute('action');
            const form = new FormData(e.target);
            const action = e.submitter.value;
            form.append("action", action); //manually adding type of action from submit button

            fetch(url, {
                method: 'POST',
                body: form,
            }).then(function (response) {
                if (response.ok) {
                    if(action === 'update'){ document.getElementById('sent').style.opacity = 1; }
                    return response.json();
                }
                return Promise.reject(response);
            }).then(function (data) {
                console.log(data);
            }).catch(function (error) {
                console.warn(error);
            });


        });
    });

    //get local IP to display 
    fetch('/getIP', { method:'POST' })
    .then( e => e.json() )
    .then( ({ip}) => {
        document.getElementById('ip').innerHTML = `URL mobile: <b>${ip}:8000</b>`;
    });

}



window.onload = __main__;