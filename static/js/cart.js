var updateBtns = document.getElementsByClassName('update-cart')


for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var teacherTimeId = this.getAttribute("data-teacherTime")
        var action = this.dataset.action
        console.log('productId:', teacherTimeId, "action:", action)
    })
}