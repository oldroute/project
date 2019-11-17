var solutionPage = function(e){
 // инициализировать ace-editor
    document.querySelectorAll('.js__editor').forEach(function(elem, index){
        var editor = ace.edit(elem.querySelector('.js__editor-ace'))
        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(true)                       // для чтения
        switch(elem.getAttribute('data-lang')){
            case 'python':
                editor.getSession().setMode("ace/mode/python"); break
            case 'cpp':
                editor.getSession().setMode("ace/mode/c_cpp"); break
            case 'csharp':
                editor.getSession().setMode("ace/mode/csharp"); break
        }
    })
}

var getUserSolutions = function(e){
    $.get(e.target.userSolutionUrl, function(response){
        for (const [key, val] of Object.entries(response)) {
            var elem = document.querySelector('#' + key)
            elem && elem.classList.add('status__' + val)
        }
        document.querySelectorAll('.js__topic-item').forEach(function(elem){
            var taskitems = elem.querySelectorAll('.js__taskitem-item')
            var taskitems_success = elem.querySelectorAll('.js__taskitem-item.status__3')
            if(taskitems.length != 0 && taskitems.length == taskitems_success.length){
                elem.classList.add('status__3')
            }
        })
    })
}

var toggleSidebar = function(){
    document.querySelectorAll('.js__topic-item').forEach(function(elem){
        var currentElem = elem.querySelector('.js__current')
        if(currentElem){
            elem.querySelector('.topic__item-toggler').classList.remove('collapsed')
            elem.querySelector('ul').classList.add('show')
        }
    })
}

window.addEventListener('solutionPageLoaded', solutionPage)
window.addEventListener('getUserSolutions', getUserSolutions)
window.addEventListener('toggleSidebar', toggleSidebar)
