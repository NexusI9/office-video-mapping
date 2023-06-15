
function __main__(){
    
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
        } )

    document.querySelectorAll('form').forEach( item => {
        
        item.addEventListener("submit", function (e) {
            e.preventDefault(); // prevent page reload
            const url = item.getAttribute('action');
            fetch(url, {
                method: 'POST',
                body: new FormData(e.target),
            }).then(function (response) {
                if (response.ok) {
                    if(url === '/update'){ document.getElementById('sent').style.opacity = 1; }
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

}



window.onload = __main__;