// sidebar
var sidebarBtns = document.querySelectorAll('.js__sidebar-btn')
sidebarBtns && sidebarBtns.forEach(function(elem){
    elem.addEventListener('click', function(e){
        e.target.classList.toggle("active")
        document.querySelector('.js__sidebar').classList.toggle("active")
    })
})

document.addEventListener('click', function(e) {
    var sidebar = document.querySelector('.js__sidebar')
    if(!sidebar.contains(e.target)){
        sidebar.classList.remove("active")
        document.querySelectorAll('.js__sidebar-btn').forEach(function(e){
            e.classList.remove('active')
        })
    }
})