function createPromptWindow() {
  let x = `
    <md-dialog id="prompt-window" style="max-width: 600px;">
        <div slot="headline" id="prompt-headline" style="text-align:center"></div>
        <md-icon slot="icon" id="prompt-icon" class="override-material-icons"></md-icon>
        <form id="prompt-form" slot="content" method="dialog">
            <p id="prompt-form-text" style="text-align:center"></p><br>
            <md-outlined-text-field label="" value="" id="prompt-form-input" style="width:100%">
            </md-outlined-text-field>
        </form>
        <div slot="actions">
          <md-text-button form="prompt-form" value="action" id="prompt-action">
          </md-text-button>
          <md-filled-tonal-button form="prompt-form" value="cancel" autofocus>
            Cancel
          </md-filled-tonal-button>
        </div>
      </md-dialog>
    `
  x = $(x);
  $("body").append(x);
  return x;
}
function promptWindow(headline, icon, label, text, action_text, default_value, callback) {
  let x = null;
  if (!((x = $('#prompt-window')).length))
    x = createPromptWindow();
  $("#prompt-headline").text(headline);
  $("#prompt-icon").text(icon);
  $("#prompt-form-text").text(text);
  $("#prompt-form-input").attr("label", label);
  $("#prompt-form-input").val(default_value);
  $("#prompt-action").text(action_text);
  x.on("close", () => {
    $(this).off("close");
    if ($("#prompt-window").prop("returnValue") == "cancel") return;
    else if ($("#prompt-window").prop("returnValue") == "action") callback($("#prompt-form-input").val());
  });
  x.attr("open", true);
}