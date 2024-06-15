// const contextmenubuttons = [
//     "Open",
//     "Download",
//     "Rename",
//     "Delete",
// ];
function updateContextMenuButtons(menu, contextmenubuttons) {
    menu.empty();
    buttons = contextmenubuttons.map(
        btn => `<md-menu-item id='cmenu-${btn.id.toLocaleLowerCase()}'>
                <div slot="headline">${btn.text}</div>
              </md-menu-item>`
    ).join('');
    buttons = $(buttons);
    menu.append(buttons);
    contextmenubuttons.forEach(btn => {
        $(`#contextmenu #cmenu-${btn.id.toLocaleLowerCase()}`).on("click", btn.action);
    });
}
function createContextMenu(id) {
    menu = `<md-menu
            id="contextmenu"
            data-id="${id}"
            anchor="body"
            tabindex='0'
            positioning="document"
            aria-label="Context menu"
            .stayOpenOnFocusout=true>
          </md-menu>`;
    menu = $(menu);
    $("body").append(menu);
    $('#contextmenu md-menu-item').on("click", () => {
        menu.attr('open', false);
    });
    return menu;
}
function showContextMenu(onto, contextmenubuttons, id) {
    let menu = null;
    if (!((menu = $('#contextmenu')).length)) {
        menu = createContextMenu(id);
    }
    if (menu.attr("data-id") != id) {
        menu.remove();
        menu = createContextMenu(id);
    }
    if (menu.attr('anchor') === onto.attr('id')) {
        menu.attr('open', !menu.attr('open'));
        return;
    }
    updateContextMenuButtons(menu, contextmenubuttons);
    menu.attr('anchor', onto.attr('id'));
    menu.attr('open', true);
}