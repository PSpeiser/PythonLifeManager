/*
 Required JS:
 jquery
 jquery.jstree
 jquery.ui

 Required HTML elements:
 #tree: that will hold the tree

 */

$(document).ready(function () {
    $.ajaxSetup({
        cache: true
    });
    $("#tree").jstree({
        "core": {
            "animation": 100
        },
        "json_data": {
            "ajax": {
                "url": "jstree.json"
            }
        },
        "themes": {
            "theme": 'classic',
            "dots": false,
            "icons": false
        },
        "plugins": [ "themes", "json_data", "ui" ] })
        .bind("dblclick.jstree", function (event) {
            var node = $(event.target).closest("li");
            testvar = node;
            if (node.hasClass('day') || node.hasClass('week')) {
                $("#tree").jstree("toggle_node", node);
            }
            else if (node.hasClass('meal')) {
                $(function () {
                    var $div = $('<div>', {id: 'dialog-confirm', title: 'Meal Deletion'})
                    $('body').append($div);
                    $div.text('Delete ' + node.text() + ' ?').dialog({
                        resizable: false,
                        height: 130,
                        modal: true,
                        buttons: {
                            "Remove meal": function () {
                                //send meal deletion here then reload json data sources
                                alert(node.attr('meal_id'));
                                $(this).dialog("close");
                            },
                            "Cancel": function () {
                                $(this).dialog("close");
                            }
                        }
                    });
                });
            }
        })
        .bind("loaded.jstree refresh.jstree", function (event, data) {
            $("#tree").find("a").each(function () {
                var parent_color = $(this).parent().attr("jstree_color")
                if (parent_color !== undefined) {
                    $(this).attr('class', parent_color);
                }
            })
        });
});