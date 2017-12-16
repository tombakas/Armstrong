$( document ).ready(function() {

    function process_dependencies() {
        var schema_raw = $("#schema").val();
        var dependencies_raw = $("#dependencies").val();

        var columns = schema_raw.split(",");
        var req_json = {};
        var dependencies = {};

        for (i = 0; i < columns.length; i++) {
            columns[i] = $.trim(columns[i]);
            if (! /^[a-zA-Z()]+$/.test(columns[i])) {
                $("#error span").text("Invalid character in \"Schema\"");
                $("#error").show();
                return;
            }
        }

        var dependencies_letters = (dependencies_raw.replace(/\W/g, ''));

        for (i = 0; i < dependencies_letters.length; i++) {
            if ($.inArray(dependencies_letters[i], columns) == -1) {
                $("#error span").text("Item \"" + dependencies_letters[i] + "\" not in schema");
                $("#error").show();
                return;
            }
        }

        var split_dependencies = dependencies_raw.split(",");

        if (dependencies_raw.length > 0) {
            for (i = 0; i < split_dependencies.length; i++) {
                var split = split_dependencies[i].split("->");

                for (k = 0; k < split.length; k++) {
                    split[k] = split[k].trim();
                }

                if (split.length != 2) {
                    $("#error span").text("Invalid dependency syntax");
                    $("#error").show();
                    return;
                }

                for (j = 0; j < split.length; j++) {
                    if (! /^[a-iA-Z()]+$/.test(split[j])) {
                        $("#error span").text("Invalid character in \"Dependencies\"");
                        $("#error").show();
                        return;
                    };

                    $("#error").hide();

                    if (!(split[0] in dependencies)) {
                        dependencies[split[0]] = split[1];
                    } else {
                        dependencies[split[0]] += split[1];
                    }
                }
            }
        }

        req_json["columns"] = columns;
        req_json["dependencies"] = dependencies;

        $.ajax({
            method: "POST",
            url: "/get-tables",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(req_json)
        })
        .done(function(response) {
            if (response.data.hasOwnProperty("errors")) {
                e = response.data.errors;
                $("#error span").empty();
                for(i = 0; i < e.length; i++) {
                    $("#error span").append(e[i]);
                }
                $("#error").show();
            } else {
                $('#tables').empty().append(response["data"]);
                MathJax.Hub.Typeset();
            }
        })
        .fail(function() {
            console.log("Error");
        })
    };

    $( "#get-armstrongs" ).click(process_dependencies);

    $("input").keyup(function(e) {
        var code = e.keyCode ? e.keyCode : e.which;
        if (code == 13) {  // Enter keycode
            e.preventDefault();
            process_dependencies();
        }
    });
});
