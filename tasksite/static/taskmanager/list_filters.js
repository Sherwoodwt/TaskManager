$(document).ready(function() {

    $('#filters').change(function() {
        if($(this).val() === '0'){
            all();
        } else if($(this).val() === 'None') {
            unassigned();
        } else {
            by_id($(this).val());
        }
    })

    function all() {
        $('.task').each(function(index, task) {
            $(task).show();
        })
    }

    function unassigned() {
        $('.task').each(function(index, task) {
            if($(task).data('value').length === 0) {
                $(task).show();
            } else {
                $(task).hide();
            }
        })
    }

    function by_id(user_id) {
        $('.task').each(function(index, task) {
            if($(task).data('value').toString() === user_id) {
                $(task).show();
            } else {
                $(task).hide();
            }
        })
    }

    $('button[type=submit]').click(function() {
        $(this).attr('disabled', 'disabled');
        $(this).parents('form').submit();
    })
})