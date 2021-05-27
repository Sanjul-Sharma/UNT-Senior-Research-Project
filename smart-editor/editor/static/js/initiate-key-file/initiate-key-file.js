/**
 * Created by Sanjul Sharma on April 22, 2021
 * All right reserved. Copyright © 2021.
 */

$(function () {
    let $key_file_name = $("form[name='import-key-file']");
    let key_file_name_ = $key_file_name.data("key-file-name");
    let secret_key_ = $key_file_name.data("secret-key");
    let has_key_file_name_ = key_file_name_ === "None" || key_file_name_ === null || key_file_name_ === undefined || key_file_name_ === "";
    let has_secret_key_ = secret_key_ === "None" || secret_key_ === null || secret_key_ === undefined || secret_key_ === "";
    if ( has_key_file_name_ && has_secret_key_ ) {
        return;
    }
    $("span[id='imported-file-name']").remove();
    $key_file_name.append(`<span style="font-size: large;" id="imported-file-name">Selected file: ${key_file_name_}</span>`);
});