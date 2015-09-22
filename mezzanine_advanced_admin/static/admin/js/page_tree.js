
jQuery(document).ready(function($) {

    var cookie = 'mezzanine-admin-tree';
    var at = ('; ' + document.cookie).indexOf('; ' + cookie + '=');
    var ids = '';

    if (at > -1) {
        ids = document.cookie.substr(at + cookie.length + 1).split(';')[0];
    }

    var toggleID = function(opened, id) {
        // Add or remove the page ID from the cookie IDs string.
        var index = $.inArray(id, ids.split(','));
        if (opened) {
            if (index == -1) {
                if (ids) {ids += ',';}
                ids += id;
            }
        } else if (index > -1) {
            ids = ids.split(',');
            ids.splice(index, 1);
            ids = ids.join(',');
        }
        document.cookie = cookie + '=' + ids + '; path=/';
    };

    function showButtonWithChildren() {
        $('ol:has(li.page)').parent().find('.tree-toggle').css({visibility: 'visible'});
        $('ol:not(:has(li.page))').parent().find('.tree-toggle').css({visibility: 'hidden'});
    }

    showButtonWithChildren();

    $('#tree .tree-toggle').click(function() {
        // Show/hide the branch and toggle the icon.
        var pageLink = $(this);
        pageLink.parents('li:first').find('ol:first').toggle();
        pageLink.find('.icon').toggle();
        // Add or remove the page ID from the cookie.
        var opened = pageLink.find('.tree-close:visible').length == 1;
        var id = pageLink.attr('id').split('-')[1];
        toggleID(opened, id);
        return false;
    });

    // Show previously opened branches.
    $('#tree ol').find('ol').hide();
    if (ids) {
        $('#page-' + ids.split(',').join(', #page-')).each(function(){
            var pageLink = $(this);
            pageLink.parents('li:first').find('ol:first').toggle();
            pageLink.find('.tree-close').show();
            pageLink.find('.tree-open').hide();
        });
    }

    $('#tree ol').find('ol:not(:has(li.page))').show();

    // The dropdown list for adding a new page contains URLs for each
    // model - redirect when selected.
    $('.addlist a').click(function(e) {
        e.preventDefault();
        // Ensure the branch is saved as open when adding to it so that
        // the new branch will be visible directly after saving.
        var link = $(this);
        var id = link.parents('.addlist:first').attr('id');
        if (id) {
            toggleID(true, id.split('-')[1]);
        }
        var addUrl = link.attr('href');
        if (addUrl) {
            location.href = addUrl;
        }
        return true;
    });

    // AJAX callback that's triggered when dragging a page to re-order
    // it has ended.
    var updateOrdering = function(event, ui) {
        var parent = ui.item.parents('li:first');

        var args = {
            id: ui.item[0].id,
            parent_id: parent.length ? parent[0].id : "null",
            siblings: ui.item.parent().children().map(function(index, elem) {
                return elem.id;
            }).get(),
            csrfmiddlewaretoken: window.__csrf_token
        };

        $.post(window.__page_ordering_url, args, function(data) {
            if (String(data).substr(0, 2) !== "ok") {
                location.reload();
            } else {
                $(".messagelist").remove();
            }
        });

        showButtonWithChildren();
    };

    // Make the pages sortable via drag and drop.
    // The `connectWith` option needs to be set separately to get
    // around a performance bug with `sortable`.
    var $tree = $('#tree > ol').nestedSortable({
        handle: '.ordering',
        opacity: 0.5,
        stop: updateOrdering,
        forcePlaceholderSize: true,
        placeholder: 'placeholder',
        revert: 150,
        helper: 'clone',
        items: 'li.page',
        tabSize: 25,
        tolerance: 'pointer',
        toleranceElement: '> div',
        isTree: true,
        expandOnHover: 1000,
        startCollapsed: true
    });

});
