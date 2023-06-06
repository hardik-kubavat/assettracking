function notifySuccess(msg) {
    $.notify({
        // options
        message: msg
    }, {
        // settings
        type: 'success',
        placement: {
            from: "top",
            align: "center"
        },
    });
}

function notifyFailure(msg) {
    $.notify({
        // options
        message: msg
    }, {
        // settings
        type: 'danger',
        placement: {
            from: "top",
            align: "right"
        },
    });
}