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

var toggleWidgetAceInput = function(e){
   if($(this).prop('checked')){
        $(this).parents('fieldset').find('.field-input').show()
   } else {
        $(this).parents('fieldset').find('.field-input').hide()
   }
}

var toggleWidget = function(e){
    var fieldset = $(this).parents('fieldset')
    if($(this).val() == 'text'){
        fieldset.find('.field-show_input').hide()
        fieldset.find('.field-input').hide()
        fieldset.find('.field-content').hide()
        fieldset.find('.field-text').show()
    } else if($(this).val() == 'ace'){
        if(fieldset.find('.field-show_input input[type=checkbox]').prop('checked')){
            fieldset.find('.field-input').show()
        } else {
            fieldset.find('.field-input').hide()
        }
        fieldset.find('.field-show_input').show()
        fieldset.find('.field-content').show()
        fieldset.find('.field-text').hide()
    }
}

$(document).ready(function(){
    aceInit()
    $('#content-group .field-type select').each(toggleWidget)

    /* инициализировать ace для нового блока кода */
    $('#content-group .add-row a').on('click', function(e){
        aceInit()
         $('#content-group .field-type select').each(toggleWidget)
         $('#content-group .field-show_input input[type=checkbox]').each(toggleWidgetAceInput)
    })

    /* Показать/скрыть блок ввода редактора */
    $(document).on('change', '#content-group .field-show_input input[type=checkbox]', toggleWidgetAceInput)

    /* Переключть тип виджета */
    $(document).on('change', '#content-group .field-type select', toggleWidget)
})
