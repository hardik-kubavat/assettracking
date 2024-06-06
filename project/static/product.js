function populateCategoryByProductType(product_type_id, category_id) {
    $("#category_id").children('option:not(:first)').remove();
    $.ajax({
        method: "get",
        url: "producttype/" + product_type_id + "/categories",
        success: function(data) {
            $.each(data, function(key, value) {
                $("#category_id").append("<option value=" + value['id'] + ">" + value['name'] + "</option>")
            });
            $("#category_id").val(category_id);
        },
        error: function() {
            notifyFailure("Error while fetching category based on the Product type. Please contact administrator");
        }
    })
}

function onDelete(product_id) {
    if (confirm("You are deleting product record. Are you sure?")) {
        $.ajax({
            method: "DELETE",
            url: "product/" + product_id,
            success: function(data) {
                $('#producttable').DataTable().ajax.reload(null, false);
                notifySuccess("Record Deleted Successfully.");
            },
            error: function() {
                notifyFailure("There is an error while processing. Contact Administrator.");
            }
        })
    }
}

function onEdit(product_id) {
    $.ajax({
        method: "get",
        url: "product/" + product_id,
        success: function(data) {
            $("#product_id").val(data.id)
            $("#product_type_id").val(data.product_type_id)
            populateCategoryByProductType(data.product_type_id, data.category_id);
            $("#srno").val(data.srno)
            $("#identification").val(data.identification)
            $("#status").val(data.status)
            $("#owner").val(data.owner)
            $("#remarks").val(data.remarks)
            $("#productmodal").modal('show');
        },
        error: function() {
            notifyFailure("There is an error while processing. Contact Administrator.");
        }
    });
}

function onAllocate(product_id, srno, currentlocater_id) {
    $("#al_product_id").val(product_id);
    $("#al_srno").val(srno)
    $("#al_locater_id").children(`option[value="${currentlocater_id}"]`).hide()
    $("#allocatemodal").modal("show");
}

function onReplace(product_id, srno, currentlocater) {
    $("#rp_product_from_id").val(product_id);
    $("#rp_from_srno").val(srno)
    $("#rp_from_locater").val(currentlocater);
    $("#replacemodal").modal("show");
}

function onShowHistory(product_id) {
    $.ajax({
        method: "get",
        url: "transaction/product/" + product_id,
        accepts: "text/html",
        success: function(data) {
            console.log(data);
            $('#historymodal').find('.modal-body').children().remove();
            $('#historymodal').find('.modal-body').append(data);
        },
        error: function(data) {
            $('#historymodal').find('.modal-body').children().remove();
            notifyFailure("There is an error while fetching data.");
            console.log(data);
        }
    });
    $('#historymodal').modal("show");

}

//When Documents loads intialize the products datatable
$(document).ready(function() {
    $url = 'product/'
    if ($page.includes("asset")){
        $url = 'product/hq'
    }
    var table = $('#producttable').DataTable({
        language: {
            searchBuilder: {
                title: {
                    0: "Filter",
                    _: "Filter (%d)"
                },
                add:  "Search Criteria",
                data: 'Column',
            }
        },
        layout:{
            topStart: 'searchBuilder'
        },
        responsive: true,
        //dom: '<"container-fluid"<"row"<"col"l><"col"B><"col"f>>>rtip',
        dom: '<"container-fluid"<"row"Q><"row"<"col"l><"col"B><"col"f>>>rtip',
        "buttons": ["excel", "pdf"],
        columnDefs: [
            { targets: "_all", className: 'text-center' },
            { "sortable": false, "targets": 0 }
        ],
        "ajax": $url,
        "columns": [{
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                "sortable": false
            },
            { "data": "producttype" },
            { "data": "category" },
            { "data": "srno" },
            { "data": "identification" },
            { "data": "currentlocation" },
            {
                "data": "status",
                render: function(data, type, row) {
                    if (data == 'WO') {
                        return "<span class='badge badge-success'>WORKING</span>"
                    } else if (data == 'NW'){
                        return "<span class='badge badge-danger'>NOT WORKING</span>"
                    } else {
                        return "<span class='badge badge-warning'>E-WASTE</span>"
                    }
                }
            },
            {"data": "ownertext"},
            {"data": "remarks"},
            {
                "data": "id",
                render: function(data, type, row) {
                    return '<div class="btn-group">'+
                    '<button class="btn btn-secondary btn-sm dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+
                      'Action'+
                    '</button>'+
                    '<div class="dropdown-menu">'+
                    '<a class="dropdown-item" href="#" onClick="onEdit(' + data + ')">Edit</a>'+
                    '<a class="dropdown-item" href="#" onclick="onAllocate(' + data + ',\'' + row.srno + '\',' + row.currentlocater_id + ')">Allocate</a>'+
                    '<a class="dropdown-item" href="#" onclick="onReplace(' + data + ',\'' + row.srno + '\',\'' + row.currentlocation + '\')">Replace</a>'+
                    '<a class="dropdown-item" href="#" onclick="onDelete(' + data + ')">Delete</a>'+
                    '<a class="dropdown-item" href="#" onclick="onShowHistory(' + data + ')">History</a>'+
                    '</div>'+
                    '</div>'
                }
            }
        ],
        order: [
            [1, 'asc'],
            [2, 'asc'],
            [3, 'asc'],
            [4, 'asc'],
            [5, 'asc'],
        ],
        "lengthMenu": [
            [100, -1],
            [100, "All"]
        ]
    });

    //Refresh Datatble on specific interval
    // setInterval(function() {
    //     $('#producttable').DataTable().ajax.reload();
    // }, 30000);
    //On change based on product type populate categories
    $("#product_type_id").on('change', function() {
        populateCategoryByProductType($("#product_type_id").val());
    });

    //When product modal show event fire set focus on first field. 
    $("#productmodal").on('shown.bs.modal', function() {
        $('#product_type_id').trigger("focus");
    });

    //When product modal's hide events fire reset form
    $('#productmodal').on('hidden.bs.modal', function() {
        $("#productform")[0].reset();
        $('#product_id').val('')
    });

    $("#allocatemodal").on('shown.bs.modal', function() {
        $('#al_locater_id').trigger("focus");
    });

    $('#allocatemodal').on('hidden.bs.modal', function() {
        $("#allocateform").trigger("reset");
        $("#al_locater_id").children().show();
    });

    $("#replacemodal").on('shown.bs.modal', function() {
        $('#rp_to_srno').trigger("focus");
    });

    $('#replacemodal').on('hidden.bs.modal', function() {
        $("#replaceform").trigger("reset");
    });

    $("#rp_to_srno").autocomplete({
        source: "product/autocomplete",
        minLength: 2,
    });

    $("#rp_to_srno").on("change", function() {
        $.ajax({
            method: "get",
            url: "product/find/" + $(this).val(),
            success: function(data) {
                $("#rp_to_locater").val(data.currentlocation)
                $("#rp_product_to_id").val(data.id)
                console.log(data);
            },
            error: function(data) {
                console.error(data);
            }
        })
    });

    $("#productuploadform").submit(function(e) {
        $("#productuploadmodal").modal("hide");
    })

    $("#productform").submit(function(e) {
        e.preventDefault();
        let formData = $(this).serialize();

        $.ajax({
            method: "post",
            url: "product/add",
            data: formData,
            success: function(data) {
                $("#productmodal").modal('hide');
                $("#productform").trigger("reset");
                $('#producttable').DataTable().ajax.reload(null, false);
                notifySuccess("Record Saved Successfully.");
                console.log(data);
            },
            error: function(data) {
                notifyFailure("There is an error while saving record." + data);
                console.log(data);
            }
        });
    });

    $("#allocateform").submit(function(e) {
        e.preventDefault();
        let formData = $(this).serialize();

        $.ajax({
            method: "post",
            url: "transaction/",
            data: formData,
            success: function(data) {
                $("#allocatemodal").modal("hide");
                $('#producttable').DataTable().ajax.reload(null, false);
                notifySuccess("Record Saved Successfully.");
                console.log(data);
            },
            error: function(data) {
                notifyFailure("There is an error while saving record.");
                console.log(data);
            }
        });
    });

    $("#replaceform").submit(function(e) {
        if ($("#rp_product_from_id").val() == $("#rp_product_to_id").val() || $("#rp_from_locater").val() == $("#rp_to_locater").val()) {
            notifyFailure("Either Asset or Locater are same.");
            return false;
        }

        e.preventDefault();
        let formData = $(this).serialize();

        $.ajax({
            method: "post",
            url: "transaction/replace",
            data: formData,
            success: function(data) {
                $("#replacemodal").modal("hide");
                $('#producttable').DataTable().ajax.reload(null, false);
                notifySuccess("Record Saved Successfully.");
                console.log(data);
            },
            error: function(data) {
                notifyFailure("There is an error while saving record.");
                console.log(data);
            }
        });
    });
});