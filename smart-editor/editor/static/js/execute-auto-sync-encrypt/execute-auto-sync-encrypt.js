/**
 * Created by Sanjul Sharma on April 22, 2021
 * All right reserved. Copyright © 2021.
 */

$(function () {
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function executeSleep(ms) {
        await sleep(ms);
    }

    function autoSyncEncrypt() {
        let $rich_text = $("div[id*='rich-text']");
        let $key_expired = $(".key-expired");
        let editor_status = parseInt($rich_text.data("editor-status"));
        if (($key_expired.length > 0) && ($key_expired.data("key-expired") === false) && (editor_status === 2)) {
            $("input[name='encrypt_save']").trigger("click");
        } else {
            if (editor_status === 2) {
                $("input[name='encrypt_save']").trigger("click");
            }
        }
    }

    function checkKeyValidity() {
        let $input_check_validity = $("input[id*='check-key-validity']");
        let $rich_text = $("div[id*='rich-text']");
        let pk_ = $rich_text.data("editor-pk");
        let key_ = $("form[name*='import-key-file']").data("secret-key");
        $.ajax({
            type: $input_check_validity.data("request-method"),
            url: $input_check_validity.data("url"),
            dataType: "json",
            data: {"pk": pk_ !== undefined || pk_ !== null || pk !== 0 || pk !== "0" ? pk_ : null, "key": key_},
            success: function (result) {
                if (result["data"]) {
                    window.location.reload(true);
                }
            },
            error: function () {
                alertify.set("notifier", "position", "top-right");
                alertify.error("Something went wrong. Please refresh manually!!!");
                console.log("Something went wrong. Please refresh manually!!!");
            }
        });
    }

    // Cron('*/10 * * * * *', function () {
    //     autoSyncEncrypt();
    // });

    Cron('0 */5 * * * *', function () {
        checkKeyValidity();
    });
});