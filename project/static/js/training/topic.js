var topicPage = function(e){

    document.querySelectorAll('.editor-form').forEach(function(form, index){

        // скрипт контрольной панели редактора кода
        var formControl = {
            aceInit: function(){
                // инициализировать ace-editor
                form.querySelectorAll('.ace-editor').forEach(function(elem, index){
                    var textarea = form.querySelector('#' + elem.getAttribute('id') + '-content'),
                        editor = ace.edit(elem.getAttribute('id')),
                        lang = form.querySelector("input[name=lang]").value

                    editor.setOption("showPrintMargin", false)     // убрать верт черту
                    editor.setOption("maxLines", "Infinity")       // авто-высота
                    editor.setHighlightActiveLine(false);          // убрать строку вделения
                    editor.setReadOnly(textarea.getAttribute('readonly'))  // для чтения
                    switch(lang){
                        case 'python':
                            editor.getSession().setMode("ace/mode/python"); break
                        case 'cpp':
                            editor.getSession().setMode("ace/mode/c_cpp"); break
                        case 'csharp':
                            editor.getSession().setMode("ace/mode/csharp"); break
                    }

                    // вписать код из textarea в ace-editor
                    var editorContent = textarea.innerHTML
                    editor.setValue(editorContent, - 1)

                    // после записи кода в ace-editor скопировать его в textarea
                    editor.addEventListener('change', function(e){
                        // если поле контента пустое то заблокировать панель редактора
                        if(textarea.getAttribute('name') == 'content'){
                            if(editor.getValue() == ''){
                                formControl.disableBtns()
                            } else {
                                formControl.enableBtns()
                            }
                        }
                    })

                    // если в редкаторе пусто то заблокировать панель редактора
                    if(textarea.getAttribute('name') == 'content' && editorContent == ''){
                        formControl.disableBtns()
                    }
                })
            },
            hideMsg: function(){ form.querySelectorAll('.msg').style('display', 'none') },
            disableBtns: function(){ form.querySelector('.control-btn').classList.add('disabled') },
            enableBtns: function(){ form.querySelector('.control-btn').classList.remove('disabled') },
            showLoader: function(msg){
                formControl.hideMsg();
                $('#msg__loader').show();
                $('#msg__loader-text').html(msg).show();
            },
            showMsg(response){
                formControl.hideMsg()
                switch(response.status){
                    case 200:
                        $('#msg__success').html(response.msg).show(); break
                    case 201:
                        $('#msg__warning').html(response.msg).show(); break
                    case 202:
                    case 203:
                    case 204:
                        $('#msg__error').html(response.msg).show(); break
                }
                setTimeout(function(){ formControl.hideMsg() }, 10000);
            },
            serializeForm(operation){
                // вернуть данные формы + submitType
                var data = {},
                    formArray = form.serializeArray();

                for (i=0; i<formArray.length; i++){
                    var value = formArray[i].value;
                    if(value){
                        data[formArray[i].name] = value;
                    }
                }
                data['operation'] = operation
                return data
            },
            debug : function(e){
                // запрос на отладку кода из редактора
                formControl.showLoader('Отладка');
                $.post(form.attr('action'), formControl.serializeForm(operation='debug'), function(response){
                    formControl.showMsg(response);
                    if(response.output){
                        $('#id-output-content').html(response.output)
                        $('.ace-output').show()
                    } else {
                        $('.ace-output').hide()
                    }
                    if(response.error){
                        $('#id-error-content').html(response.error)
                        $('.ace-error').show()
                    } else {
                        $('.ace-error').hide()
                    }
                    formControl.aceInit();
                });
                return false;
            }
        }

        formControl.aceInit()

        // Обработчики кнопок
        /*
        document.querySelector('#editor__debug-btn').addEventListener('click', formControl.debug)
        */
    })
}

window.addEventListener('topicPageLoaded', topicPage)