function deleteFlash(flash) {
    $(flash).parent().remove();
}

function radioDependency(radio) {
    switch (radio.id) {
        case "ehyp-init":
            $("#ehyp-to").prop("checked", false);

            $("#ehyp-to").prop("disabled", true);
            $("#qp-to").prop("disabled", false);
            $("#bfx-to").prop("disabled", false);
            break;
        case "qp-init":
            $("#qp-to").prop("checked", false);

            $("#ehyp-to").prop("disabled", false);
            $("#qp-to").prop("disabled", true);
            $("#bfx-to").prop("disabled", false);
            break;
        case "bfx-init":
            $("#bfx-to").prop("checked", false);

            $("#ehyp-to").prop("disabled", false);
            $("#qp-to").prop("disabled", false);
            $("#bfx-to").prop("disabled", true);
            break;
    }
}
