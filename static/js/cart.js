var updateBtns = document.getElementsByClassName('update-cart')


for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var teacherTimeId = this.getAttribute("data-teacherTime")
        var action = this.dataset.action
        console.log('productId:', teacherTimeId, "action:", action)
        if (user === 'AnonymousUser') {
            console.log('Not logged in')
        }else{
            updateUseOrder(teacherTimeId, action)
        }
    })
}

function updateUseOrder(teacherTimeId, action) {
    console.log('user is logged in, sending data...')

    var url = '/shop/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'teacherTimeId': teacherTimeId, 'action':action})
    })

        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data', data)
        })
}