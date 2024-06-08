function askDownload(filename, filePath) {
    if (confirm('The file is too big. Do you want to download it?')) {
        const element = document.createElement('a');
        element.setAttribute('href', filePath);
        element.setAttribute('style', 'display:none')
        element.setAttribute('download', filename);
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
}
function renameFileObject(fileObject) {
    const newName = prompt(`What you want to rename ${fileObject} to?`, fileObject);
    if (newName == null) return;
    fetch(`?rename=${fileObject}:${newName}`).catch(function (err) {
        console.error('Fetch Error :-S', err);
    });
    window.location.reload();
}
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}
function setCookie(name, value, options = {}) {

    options = {
        path: '/',
        ...options
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}
function deleteCookie(name) {
    setCookie(name, "", {
        'max-age': -1
    })
}
function showError(errorInfo) {

}
function loadFolder() {
    $('#fileview').empty();
    let fpath = getCookie("fpath");
    if (typeof (fpath) == "undefined") {
        fpath = "";
        setCookie("fpath", fpath);
    }
    $("#address-bar-path").val(fpath.substring(1));
    fetch("/api/get-folder", {
        method: "POST",
        body: JSON.stringify({
            path: fpath
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then((response) => response.json()).then((json) => {
        let data = json;
        if (data.result == "error") {
            showError(data.cause);
            return;
        }
        data = data.data;
        data.forEach(file => {
            let result = `<div class="card surface" data-id="${file.name}">${file.icon}<h3>${file.name}</h3>`;
            if (!file.is_folder)
                result += `<i>${file.size}</i>`;
            result += "</div>";
            result = $(result);
            if (!file.is_folder)
                result.on("dblclick", function () {
                    window.location.assign("/$pbl" + fpath + "/" + file.name);
                });
            else
                result.on("dblclick", function () {
                    setCookie("fpath", fpath + "/" + result.attr("data-id"));
                    loadFolder();
                });
            $("#fileview").append(result);
        });
    });
}
$(document).ready(function () {
    $("#address-bar-path").keypress(function (e) {
        if (e.which == 13) {
            setCookie("fpath", "/" + $(this).val());
            loadFolder();
            return false;
        }
    });
    $("#address-bar-back-button").on("click", function () {
        let fpath = getCookie("fpath");
        if (typeof (fpath) == "undefined") {
            fpath = "";
            setCookie("fpath", fpath);
        }
        setCookie("fpath", fpath.split('/').slice(0, -1).join("/"));
        loadFolder();
    });
    $("#address-bar-home-button").on("click", function () {
        setCookie("fpath", "");
        loadFolder();
    });
    loadFolder();
});