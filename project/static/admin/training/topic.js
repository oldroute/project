var aceInit = function(){
    $('.ace-editor').each(function(){
        var id = '#' + $(this).attr('id'),
            textarea = $(id + '-content'),
            editor = ace.edit($(this).attr('id'))
            lang = JSON.parse($('.ace-config').html()).lang;
        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(textarea.attr('readonly'))  // для чтения
        switch(lang){
            case 'python':
                editor.getSession().setMode("ace/mode/python"); break
            case 'cpp':
                editor.getSession().setMode("ace/mode/c_cpp"); break
            case 'csharp':
                editor.getSession().setMode("ace/mode/csharp"); break
        }

        // вписать код из textarea в ace-editor
        var editorContent = textarea.text() ? textarea.text() : ""
        editor.setValue(editorContent, - 1)

        // после записи кода в ace-editor скопировать его в textarea
        editor.on("change", function(e){
            textarea.text(editor.getValue());
        })

    })
}

var showSelectedWidget = function(){
    $('#content-group .field-type select').each(function(e){
        if($(this).val() == 'text'){
            $(this).parents('fieldset').find('.field-ace').hide()
            $(this).parents('fieldset').find('.field-text').show()
        } else if($(this).val() == 'ace'){
            $(this).parents('fieldset').find('.field-ace').show()
            $(this).parents('fieldset').find('.field-text').hide()
        }
    })
}

$(document).ready(function(){
    aceInit()
    showSelectedWidget()
    /* инициализировать ace для нового блока кода */
    $('#content-group .add-row a').on('click', function(e){
        aceInit()
        showSelectedWidget()
    })

    /* Переключть тип виджета */
    $(document).on('change', '#content-group .field-type select', function(e){
        if($(this).val() == 'text'){
            $(this).parents('fieldset').find('.field-ace').hide()
            $(this).parents('fieldset').find('.field-text').show()
        } else if($(this).val() == 'ace'){
            $(this).parents('fieldset').find('.field-ace').show()
            $(this).parents('fieldset').find('.field-text').hide()
        }
    })
})
