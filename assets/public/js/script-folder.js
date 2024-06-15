// function askDownload(filename, filePath) {
//     if (confirm('The file is too big. Do you want to download it?')) {
//         const element = document.createElement('a');
//         element.setAttribute('href', filePath);
//         element.setAttribute('style', 'display:none')
//         element.setAttribute('download', filename);
//         document.body.appendChild(element);
//         element.click();
//         document.body.removeChild(element);
//     }
// }
function reloadFolder() {
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
        if (data.length == 0) {
            $("#fileview").append($(`
                <div class="card surface" id="empty-folder-card" data-id="">
                    <md-icon class="override-material-icons" style="font-size:128px;width:128px;height:128px;">search_off</md-icon>
                    <h2>The folder is empty<h2>
                    <md-filled-tonal-button id="empty-folder-home-button">
                        Home
                    </md-filled-tonal-button>
                    <md-filled-tonal-button id="empty-folder-back-button">
                        Back
                    </md-filled-tonal-button>
                </div>
            `));
            $("#empty-folder-back-button").off("click");
            $("#empty-folder-back-button").on("click", go_back);
            $("#empty-folder-home-button").off("click");
            $("#empty-folder-home-button").on("click", go_home);
            return;
        }
        let index = 0;
        data.forEach(file => {
            let result = `<div class="card surface" id="file_${index}" data-id="${file.name}">${file.icon}<h3>${file.name}</h3>`;
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
                    reloadFolder();
                });
            result.on("rightclick", function () {
                showContextMenu($(this), [
                    {
                        "id": "open",
                        "text": "Open",
                        "action": () => { }
                    },
                    {
                        "id": "download",
                        "text": "Download",
                        "action": () => { }
                    },
                    {
                        "id": "rename",
                        "text": "Rename",
                        "action": () => renameFileObject($(this))
                    },
                    {
                        "id": "delete",
                        "text": "Delete",
                        "action": () => deleteFileObject($(this))
                    }
                ], "file-actions");
            });
            $("#fileview").append(result);
            index += 1;
        });
    });
}
function renameFileObject(fileObject) {
    if (fileObject === null) return;
    let fpath = getCookie("fpath");
    if (typeof (fpath) == "undefined") {
        fpath = "";
        setCookie("fpath", fpath);
    }
    promptWindow(`Rename`, "new_window", "New name", `What you want to rename "${fileObject.attr('data-id')}" to?`, "Rename", fileObject.attr('data-id'), (newName) => {
        fetch(`/api/rename`, {
            method: "POST",
            body: JSON.stringify({
                path: fpath,
                original: fileObject.attr('data-id'),
                new: newName
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then((response) => response.json()).then((json) => {
            let data = json;
            if (data.result == "ok") {
                showMessage(`Renamed file ${fileObject.attr('data-id')} to ${newName} successfully!`)
            }
            else {
                showError(data.cause);
                return;
            }
        }).catch(function (err) {
            console.error('Fetch Error :-S', err);
        }).finally(function () {
            reloadFolder();
        });
    });

}
function deleteFileObject(fileObject) {
    if (fileObject === null) return;
    let fpath = getCookie("fpath");
    if (typeof (fpath) == "undefined") {
        fpath = "";
        setCookie("fpath", fpath);
    }
    confirmWindow("Permanently delete?", "delete_forever", "Deleting the file cannot be reversed.", "Delete", () => {
        fetch(`/api/delete`, {
            method: "POST",
            body: JSON.stringify({
                path: fpath,
                file: fileObject.attr('data-id')
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then((response) => response.json()).then((json) => {
            let data = json;
            if (data.result == "ok") {
                showMessage(`Deleted file ${fileObject.attr('data-id')} successfully!`)
            }
            else {
                showError(data.cause);
                return;
            }
        }).catch(function (err) {
            console.error('Fetch Error :-S', err);
        }).finally(function () {
            reloadFolder();
        });
    });
}
function go_back() {
    let fpath = getCookie("fpath");
    if (typeof (fpath) == "undefined") {
        fpath = "";
        setCookie("fpath", fpath);
    }
    setCookie("fpath", fpath.split('/').slice(0, -1).join("/"));
    reloadFolder();
}
function go_home() {
    setCookie("fpath", "");
    reloadFolder();
}
function update_buttons() {
    $("#address-bar-back-button").off("click");
    $("#address-bar-back-button").on("click", go_back);
    $("#address-bar-home-button").off("click");
    $("#address-bar-home-button").on("click", go_home);
    $("#address-bar-refresh-button").off("click");
    $("#address-bar-refresh-button").on("click", reloadFolder);
}
$(document).ready(function () {
    $.event.special.rightclick = {
        bindType: "mousedown",
        delegateType: "mousedown",
        handle: function (evt) {
            if (evt.button === 2) {
                var handleObj = evt.handleObj;
                $(document).one('contextmenu', false);
                evt.type = handleObj.origType;
                ret = handleObj.handler.apply(this, arguments);
                evt.type = handleObj.type;
                return ret;
            }
        }
    };
    $("#address-bar-path").keypress((e) => {
        if (e.which == 13) {
            setCookie("fpath", "/" + $(this).val());
            reloadFolder();
            return false;
        }
    });
    update_buttons();
    reloadFolder();
});