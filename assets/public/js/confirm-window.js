function createConfirmWindow() {
  let x = `
    <md-dialog id="confirm-window" style="max-width: 400px;">
        <div slot="headline" id="confirm-headline" style="text-align:center"></div>
        <md-icon slot="icon" id="confirm-icon" class="override-material-icons"></md-icon>
        <form id="confirm-form" slot="content" method="dialog" style="text-align:center">
        </form>
        <div slot="actions">
          <md-text-button form="confirm-form" value="action" id="confirm-action">
          </md-text-button>
          <md-filled-tonal-button form="confirm-form" value="cancel" autofocus>
            Cancel
          </md-filled-tonal-button>
        </div>
      </md-dialog>
    `
  x = $(x);
  $("body").append(x);
  return x;
}
function confirmWindow(headline, icon, text, action_text, callback) {
  let x = null;
  if (!((x = $('#confirm-window')).length))
    x = createConfirmWindow();
  $("#confirm-headline").text(headline);
  $("#confirm-icon").text(icon);
  $("#confirm-form").text(text);
  $("#confirm-action").text(action_text);
  x.on("close", () => {
    $(this).off("close");
    if ($("#confirm-window").prop("returnValue") == "cancel") return;
    else if ($("#confirm-window").prop("returnValue") == "action") callback();
  });
  x.attr("open", true);
}