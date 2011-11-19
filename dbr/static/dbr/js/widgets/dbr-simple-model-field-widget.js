(function ($) {
    $(function() {
        var fields_select = $(".dbr-model-field-select");
        var models_select = $("#id_model");

        var clear_fields_select = function() {
            fields_select.each(function () {
                $(this).change();
                $(this).html("    <option value=\"\">---------</option>");
                $(this).attr("disabled", true)
                    .attr("title", "Please choose a model before setting this option");
            });
        };

        var get_from_cache_or_fetch = function (key_name, url) {
            // Use a cache to reduce requests
            var data;
            if (sessionStorage != undefined) {
                data = sessionStorage.getItem(key_name);
            } else {
                data = document[key_name];
            };
            data = JSON.parse(data);
            if (!data) {
                // Model fields are not in cache
                $.ajax({
                    async: false, // IMPORTANT: If async, some browsers will continue over the
                    // event handlers even if the request hasn't finished
                    dataType: "json",
                    success : function (resp_data) {
                        if (sessionStorage !== undefined) {
                            sessionStorage.setItem(key_name, JSON.stringify(resp_data));
                        } else {
                            document[key_name] = JSON.stringify(resp_data);
                        };
                        data = resp_data;
                    },
                    error : function (xhr, textStatus) {
                        alert("Error getting field options\n" + textStatus);
                        data = [];
                    },
                    type: "GET",
                    url: url
                });
            };
            return data;
        };

        var populate_fields_select = function (model_name, element) {
            if (model_name !== "") {
                var url = element.attr("data-fields-options-url") + "?m=" + model_name;
                var key_name = model_name + "_fields";
                var data = get_from_cache_or_fetch(key_name, url);
                element.change();
                element.html("    <option value=\"\">---------</option>");
                element.attr("disabled", true)
                    .attr("title", "Please choose a model before setting this option");
                $.each(data, function (i, obj) {
                    var previous_value = element.parents(".inline-related").find(".inline_label").text();
                    var opt = document.createElement("option");
                    opt.text = obj.text;
                    opt.value = obj.value;
                    if (obj.text == previous_value) {
                        opt.selected = "selected";
                    }
                    element.append(opt);
                });
                element.attr("disabled", false)
                    .attr("title", "Select the model field");
            };
        };

        var on_model_change = function () {
            clear_fields_select();
            if(models_select.val() !== "") {
                fields_select.attr("disabled", false)
                    .attr("title", "Select the model field");
            }
        };

        var on_fields_focus = function () {
            var model_name = models_select.val();
            if ($(this).val() == ""){
                var fields_select = $(this);
                populate_fields_select(model_name, fields_select);
            }
        };

        fields_select.focus(on_fields_focus);
        models_select.change(on_model_change);

        if (models_select.val() == "") {
            // The form is new
            clear_fields_select();
        } else {
            // The form is bound, prepopulate.
            fields_select.each(function () {
                populate_fields_select(models_select.val(), $(this));
            });
        };
    });
})(django.jQuery);
