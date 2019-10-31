var solutionPage = function(e){
 // инициализировать ace-editor
    $('.ace-editor').each(function(){
        var editor = ace.edit($(this).attr('id')),
            lang = $(this).attr('data-lang')
        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(true)                       // для чтения
        switch(lang){
            case 'python':
                editor.getSession().setMode("ace/mode/python"); break
            case 'cpp':
                editor.getSession().setMode("ace/mode/c_cpp"); break
            case 'csharp':
                editor.getSession().setMode("ace/mode/csharp"); break
        }
    })
}

window.addEventListener('solutionPageLoaded', solutionPage)