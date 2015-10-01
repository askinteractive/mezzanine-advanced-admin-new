jQuery(function ($) {
    // Apply drag and drop to sortable inlines.
    $('.results tbody').sortable({handle: '.ordering', axis: 'y', opacity: '.4',
                                placeholder: 'sortable-placeholder'});
    $('.ordering').css({cursor: 'move'}).append($('<span>', {'class': 'mdi-action-swap-vert'}));

    // Set the value of the _order fields on submit.
    $('#changelist-form').on("submit", function() {
        $.each($('.results tbody tr'), function(i, parent) {
            $(this).find('[name$=_order]').val(i);
        });
    });
});