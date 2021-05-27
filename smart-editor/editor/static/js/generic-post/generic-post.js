/**
 * Created by Sanjul Sharma on April 22, 2021
 * All right reserved. Copyright © 2021.
 */

$(function () {
    function download(filename, text) {
        let el = document.createElement('a');
        el.setAttribute('href', 'data:application/octet-stream,' + text);
        el.setAttribute('download', filename);

        el.style.display = 'none';
        document.body.appendChild(el);

        el.click();

        document.body.removeChild(el);
    }

    function makeUID(length) {
        let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        let charactersLength = characters.length;
        let result = "";
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }

    tinymce.init({
        selector: '.rich-text-area',
        height: "80vh",
        branding: false,
        plugins: 'print preview paste importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars emoticons',
        imagetools_cors_hosts: ['picsum.photos'],
        menubar: 'file edit view insert format tools table help',
        toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',
        toolbar_sticky: true,
        autosave_ask_before_unload: true,
        autosave_interval: '30s',
        autosave_prefix: '{path}{query}-{id}-',
        autosave_restore_when_empty: false,
        autosave_retention: '2m',
        image_advtab: true,
        importcss_append: true,
        image_caption: true,
        quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
        noneditable_noneditable_class: 'mceNonEditable',
        toolbar_mode: 'sliding',
        contextmenu: 'link image imagetools table',
        content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
        add_form_submit_trigger: true,
        setup: function (editor) {
            // Let the editor save every change to the textarea
            editor.on('change', function () {
                tinymce.triggerSave();
            });

            // Do nothing when submitting the form
            editor.on('submit', function () {
                return false;
            });

            editor.on("init", function () {
                editor.getContainer().className += ' with-border';
                let txt_ = $("#rich-text").data("editor-txt");
                editor.setContent(txt_);
                // editor.setContent($(jQuery.parseHTML(txt_)).text());
            });
        }
    });

    function initiateAjaxToEncryptAndSave($rich_text, pk_, key_, key_file_name, encryptedAES) {
        $.ajax({
            type: $rich_text.data("method"),
            url: $rich_text.data("action"),
            dataType: "json",
            data: {
                "editor_text": encryptedAES,
                "pk": pk_ !== undefined || pk_ !== null || pk !== 0 || pk !== "0" ? pk_ : null,
                "key": key_, "key_file_name": key_file_name
            },
            success: function (result) {
                alertify.set("notifier", "position", "top-right");
                alertify.success(result["data"]["msg"]);
                $rich_text.data("editor-status", 2);
                if (result["data"]["key_expired"] === false) {
                    let $key_expired = $(".key-expired");
                    $key_expired.hide();
                    $key_expired.data("key-expired", false);
                }
                console.log(result["result"]);
            },
            error: function () {
                alertify.set("notifier", "position", "top-right");
                alertify.error("couldn't encrypt!!!");
                console.log("couldn't encrypt!!!");
            }
        });
    }

    function initiateAjaxToDecrypt($rich_text, pk_, csrf_token, key_) {
        $.ajax({
            type: $rich_text.data("method"),
            url: $rich_text.data("action") + "?key_validation=1",
            dataType: "json",
            data: {
                "key": key_,
                "pk": pk_ !== undefined || pk_ !== null || pk !== 0 || pk !== "0" ? pk_ : null
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (result) {
                if (result["result"] === "Success") {
                    let editor_text_content = $rich_text.data("editor-txt");
                    let decryptedBytes = CryptoJS.AES.decrypt(editor_text_content, key_);
                    let plaintext = decryptedBytes.toString(CryptoJS.enc.Utf8);
                    tinyMCE.get("id_editor_text").setContent(plaintext);
                    $rich_text.data("editor-status", 2);
                    alertify.set("notifier", "position", "top-right");
                    alertify.warning(result["data"]["msg"]);
                } else if (result["result"] === "Error") {
                    alertify.set("notifier", "position", "top-right");
                    alertify.error(result["message"]);
                    console.log(result["message"]);
                }
            },
            error: function () {
                alertify.set("notifier", "position", "top-right");
                alertify.error("couldn't decrypt!!!");
                console.log("couldn't decrypt!!!")
            }
        });
    }

    $("input[name='encrypt_save']").off("click").on("click", function () {
        let file = $("input[type='file']")[0].files[0];
        let $rich_text = $("div[id*='rich-text']");
        let pk_ = $rich_text.data("editor-pk");
        let editor_text_content = tinyMCE.get('id_editor_text').getContent();
        if (file === null || file === undefined || file === "") {
            let $key_file_name = $("form[name='import-key-file']");
            let key_file_name_ = $key_file_name.data("key-file-name");
            let secret_key_ = $key_file_name.data("secret-key");
            let has_key_file_name_ = key_file_name_ === "None" || key_file_name_ === null || key_file_name_ === undefined || key_file_name_ === "";
            let has_secret_key_ = secret_key_ === "None" || secret_key_ === null || secret_key_ === undefined || secret_key_ === "";
            if (has_key_file_name_ && has_secret_key_) {
                return;
            }
            let key_ = $key_file_name.data("secret-key");
            let encryptedAES = CryptoJS.AES.encrypt(editor_text_content, key_).toString();
            // let encryptedAES = encodeURIComponent(encryptedAES_);
            initiateAjaxToEncryptAndSave($rich_text, pk_, key_, key_file_name_, encryptedAES);
        } else {
            let fileReader = new FileReader();
            fileReader.readAsText(file);
            let key_ = null;
            fileReader.onload = function () {
                key_ = fileReader.result;
                let encryptedAES = CryptoJS.AES.encrypt(editor_text_content, key_).toString();
                // let encryptedAES = encodeURIComponent(encryptedAES_);
                initiateAjaxToEncryptAndSave($rich_text, pk_, key_, file.name, encryptedAES);

            };
        }
    });

    $("input[name='decrypt']").off("click").on("click", function () {
        let file = $("input[type='file']")[0].files[0];
        let $rich_text = $("div[id*='rich-text']");
        let pk_ = $rich_text.data("editor-pk");
        let csrf_token = $rich_text.data("csrf-token");
        if (file === null || file === undefined || file === "") {
            let $key_file_name = $("form[name='import-key-file']");
            let key_file_name_ = $key_file_name.data("key-file-name");
            let secret_key_ = $key_file_name.data("secret-key");
            let has_key_file_name_ = key_file_name_ === "None" || key_file_name_ === null || key_file_name_ === undefined || key_file_name_ === "";
            let has_secret_key_ = secret_key_ === "None" || secret_key_ === null || secret_key_ === undefined || secret_key_ === "";
            if (has_key_file_name_ && has_secret_key_) {
                return;
            }
            let key_ = $key_file_name.data("secret-key");
            initiateAjaxToDecrypt($rich_text, pk_, csrf_token, key_);
        } else {
            let fileReader = new FileReader();
            fileReader.readAsText(file);
            let key_ = null;
            fileReader.onload = function () {
                key_ = fileReader.result;
                initiateAjaxToDecrypt($rich_text, pk_, csrf_token, key_);
            };
        }
    });

    $("input[type='file']").off("change").on("change", function () {
        let file = $(this)[0].files[0];
        $("span[id='imported-file-name']").remove();
        $("form[name='import-key-file']").append(`<span style="font-size: large;" id="imported-file-name">Selected file: ${file.name}</span>`);
    });

    $("input[id='import_key_file']").off("click").on("click", function (event) {
        event.preventDefault();
        let $file_input = $("input[type='file']");
        $file_input.trigger("click");
        // let formData = new FormData($("form[name='import-key-file']")[0]);
    });

    $("input[name='generate_key_file']").off("click").on("click", function () {
        let uid_ = makeUID(1000);
        download("secret-key.key", uid_);
        alertify.set("notifier", "position", "top-right");
        alertify.success("Key file generated");
    });
});