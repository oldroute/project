var taskItemPage = function(e){

    var lastChanges = ''
    var form = $('#editor__form')
    // скрипт контрольной панели редактора кода
    var formControl = {
        aceInit: function(){
            // инициализировать ace-editor
            $('.ace-editor').each(function(){
                var id = '#' + $(this).attr('id'),
                    textarea = $(id + '-content'),
                    editor = ace.edit($(this).attr('id')),
                    lang = form.find("#id_lang").val()
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
                    // если поле контента пустое то заблокировать панель редактора
                    if(id == '#id-content'){
                        if(textarea.val().trim().length == 0){
                            formControl.disableBtns()
                        } else {
                            formControl.enableBtns()
                        }
                    }
                })

                // если в редкаторе пусто то заблокировать панель редактора
                if(id == '#id-content' && editorContent == ''){
                    formControl.disableBtns()
                }
            })
        },
        hideMsg: function(){ $('.msg').hide() },
        disableBtns: function(){ form.find('.control-btn').addClass('disabled') },
        enableBtns: function(){ form.find('.control-btn').removeClass('disabled') },
        enableVersionsBtn: function(){ form.find('.control-btn.versions').removeClass('not-versions')},
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
        },
        tests : function(e){
            formControl.disableBtns();
            formControl.showLoader('Тестирование');
            $.post(form.attr('action'), formControl.serializeForm(operation='tests'), function(response){
                formControl.showMsg(response)
                formControl.enableVersionsBtn()
                if(response.tests_result){
                    $('th.form__test-result').html('Вывод программы')
                    response.tests_result.data.forEach(function(elem, index){
                        var tr = $('#form__test-'+ index)
                        if(elem.success){
                            tr.removeClass('success unluck').addClass('success')
                        } else {
                            tr.removeClass('success unluck').addClass('unluck')
                        }
                        tr.find('.form__test-result pre').html(elem.output + elem.error)
                    })
                    if(response.tests_result.success){
                        if(!document.querySelector('h1 .success')){
                            var span = document.createElement('span')
                            span.classList.add('success')
                            span.textContent = 'Решено'
                            document.querySelector('h1').appendChild(span)

                        }
                    }
                }
                if(response.success){
                    // ...
                }
                formControl.aceInit();

            });
            return false;
        },
        version: function(e){
            formControl.showLoader('Сохранение версии')
            $.post(form.attr('action'), formControl.serializeForm(operation='create_version'), function(response){
                formControl.showMsg(response);
                formControl.enableVersionsBtn();
            });
            return false;

        },
        save: function(e){
            formControl.showLoader('Сохранение');
            $.post(form.attr('action'), formControl.serializeForm(operation='save_last_changes'), function(response){
                formControl.showMsg(response);
                formControl.enableVersionsBtn();
            });
            return false;
        },
        autosave: function(e){
            formControl.showLoader('Сохранение')
            $.post(form.attr('action'), formControl.serializeForm(operation='save_last_changes'), function(response){
                formControl.showMsg(response);
                formControl.enableVersionsBtn();
            });
            return false;
        }
    }

    formControl.aceInit()
    // Автосохранение раз в 3 мин. при условии что решение изменялось
    window.setInterval(function(){
        newChanges = $('#id-content-content').first().text();
        var versionsBtn = $('.control-btn.save-version').first();
        if(newChanges != lastChanges && versionsBtn != undefined){
            formControl.autosave();
            lastChanges = newChanges
        }
    }, 180000)

    // Обработчики кнопок
    var debugBtn = document.querySelector('#editor__debug-btn')
    debugBtn && debugBtn.addEventListener('click', formControl.debug)

    var testsBtn = document.querySelector('#editor__tests-btn')
    testsBtn && testsBtn.addEventListener('click', formControl.tests)

    var versionBtn = document.querySelector('#editor__create-version-btn')
    versionBtn && versionBtn.addEventListener('click', formControl.version)

    var saveBtn = document.querySelector('#editor__save-last-changes-btn')
    saveBtn && saveBtn.addEventListener('click', formControl.save)
}

window.addEventListener('taskItemPageLoaded', taskItemPage)