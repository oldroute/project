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
                    editor = ace.edit($(this).attr('id'))
                editor.setOption("showPrintMargin", false)     // убрать верт черту
                editor.setOption("maxLines", "Infinity")       // авто-высота
                editor.setHighlightActiveLine(false);          // убрать строку вделения
                editor.setReadOnly(textarea.attr('readonly'))  // для чтения

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
        hideMsg: function(){ form.find('.msg').addClass('hide') },
        disableBtns: function(){ form.find('.control-btn').addClass('disabled') },
        enableBtns: function(){ form.find('.control-btn').removeClass('disabled') },
        enableVersionsBtn: function(){ form.find('.control-btn.versions').removeClass('not-versions')},
        showLoader: function(msg){
            formControl.hideMsg();
            form.find('.loader').first().removeClass('hide');
            form.find('.msg-loader').first().html(msg).removeClass('hide');
        },
        showMsg(msg, status){
            formControl.hideMsg(form)
            switch(status){
                case 'success':
                    form.find('.msg-success').first().html(msg).removeClass('hide');
                    break
                case 'warning':
                    form.find('.msg-warning').first().html(msg).removeClass('hide');
                    break
                case 'error':
                    form.find('.msg-error').first().html(msg).removeClass('hide');
                    break
            }
            setTimeout(function(){ formControl.hideMsg() }, 10000);
        },
        serializeForm(submitType){
            // вернуть данные формы + submitType
            var data = {},
                formArray = form.serializeArray();

            for (i=0; i<formArray.length; i++){
                var value = formArray[i].value;
                if(value){
                    data[formArray[i].name] = value;
                }
            }
            data['submitType'] = submitType
            return data
        },
        execute : function(e){
            // запрос на отладку кода из редактора
            formControl.disableBtns();
            formControl.showLoader('Отладка');
            $.post(form.attr('action'), formControl.serializeForm('execute'), function(response, textStatus){
                formControl.showMsg(response.msg, response.status);
                form.find('.ace-input div').first().replaceWith(response.input).show();
                form.find('.ace-content div').first().replaceWith(response.content).show();
                form.find('.ace-output div').first().replaceWith(response.output).show();
                form.find('.ace-error div').first().replaceWith(response.error).show();
                formControl.aceInit();
                formControl.enableBtns(form);
            });
            return false;
        },
        tests : function(e){
            formControl.disableBtns();
            formControl.showLoader('Тестирование');
            $.post(form.attr('action'), formControl.serializeForm('tests'), function(response, textStatus){
                formControl.showMsg(response.msg, response.status);
                form.find('.ace-input div').first().replaceWith(response.input).show();
                form.find('.ace-content div').first().replaceWith(response.content).show();
                form.find('.ace-output div').first().replaceWith(response.output).show();
                form.find('.ace-error div').first().replaceWith(response.error).show();
                $('#form__tests-table').replaceWith(response.tests).show();
                formControl.aceInit();
                formControl.enableBtns(form);
                formControl.enableVersionsBtn(form);
            });
            return false;
        },
        saveVersion: function(e){
            formControl.disableBtns()
            formControl.showLoader('Сохранение')
            $.post(form.attr('action'), formControl.serializeForm('saveVersion'), function(response, textStatus){
                formControl.showMsg(response.msg, response.status);
                formControl.enableBtns();
                formControl.enableVersionsBtn();
            });
            return false;

        },
        fastSave: function(e){
            formControl.disableBtns();
            formControl.showLoader('Сохранение');
            $.post(form.attr('action'), formControl.serializeForm('fastSave'), function(response, textStatus){
                formControl.showMsg('Изменения сохранены', response.status);
                formControl.enableBtns();
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
            formControl.fastSave();
            lastChanges = newChanges
        }
    }, 180000)

    // Обработчики кнопок
    document.querySelector('#editor__execute-btn').addEventListener('click', formControl.execute)
    document.querySelector('#editor__tests-btn').addEventListener('click', formControl.tests)
    document.querySelector('#editor__save-version-btn').addEventListener('click', formControl.saveVersion)
    document.querySelector('#editor__fast-save-btn').addEventListener('click', formControl.fastSave)
}

window.addEventListener('taskItemPageLoaded', taskItemPage)