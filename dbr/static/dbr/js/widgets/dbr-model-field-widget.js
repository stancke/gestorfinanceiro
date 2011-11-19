(function ($) {
    $(function() {
        var fields_select = $(".dbr-model-fields-choice");
        var formats_select = $(".dbr-model-fields-format");
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
                    var opt = document.createElement("option");
                    opt.text = obj.text;
                    opt.value = obj.value;
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

        var on_fields_change = function () {
            $(this).next().hide();
            if ($(this).val()) {
                var element = $(this);
                var key_name = element.val() + "_summary_opts";
                var url = element.attr("data-summary-options-url") + "?f=" + element.val();
                var data = get_from_cache_or_fetch(key_name, url);
                // Set default value
                if (data.length > 0) {
                    $.each(data, function (i, obj) {
                        var opt = document.createElement("option");
                        opt.text = obj.text;
                        opt.value = obj.value;
                        element.next().append(opt);
                    });
                    $(this).next().show();
                } else {
                    var opt = document.createElement("option");
                    opt.text = "---------";
                    opt.value = "";
                    element.next().append(opt);
                    $(opt).attr("selected", true);
                }
            }
        };

        fields_select.change(on_fields_change);
        fields_select.focus(on_fields_focus);
        models_select.change(on_model_change);

        if (models_select.val() == "") {
            // The form is new
            clear_fields_select();
        } else {
            // The form is bound, prepopulate.
            fields_select.each(function () {
                populate_fields_select(models_select.val(), $(this));
                var old_value_full = $("#id_" + $(this).attr("name").split("_")[0] + "_oldvalue").val();
                if (old_value_full) {
                    console.log("old_value > " + old_value_full);
                    var old_value = old_value_full.split(",")[0];
                    $(this).val(old_value);
                    $(this).change();
                    $(this).next().val(old_value_full.split(",")[1]);
                    $(this).next().change();
                };
            });
        };
    });
})(django.jQuery);
