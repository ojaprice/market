const updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:', productId, 'Action', action)
        console.log("User:", user)
        if(user === "AnonymousUser"){
            addCookieItem(productId, action)
        }else{
            updateuserOrder(productId, action)
        }
    })
}

// for unanthenticated users 
function addCookieItem(productId, action){
    console.log("User not logged in...")
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Item should be removed')
            delete cart[productId]
        }
    }
    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateuserOrder(productId, action){
    console.log("User is logged in. Sending data")
    let url = '/update_item/'
    fetch(url, {
        method:"POST",
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) => {
        console.log('data:', data);
        location.reload()
    })
}
