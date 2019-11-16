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
    console.log()
    $.get(e.target.userSolutionUrl, function(response){
        for (const [key, val] of Object.entries(response)) {
            var elem = document.querySelector('#' + key)
            elem && elem.classList.add('status__' + val)
        }
    })
}

window.addEventListener('solutionPageLoaded', solutionPage)
window.addEventListener('getUserSolutions', getUserSolutions)