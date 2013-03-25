'use strict';

/* Nebulous Adventure */


(function (root, $) {

    var $console = $('.console div.content'),
        $scroll = $('.console'),
        $prompt = $('#prompt'),
        command = function command(text) {
            $('<pre>')
                .text('> ' + text)
                .appendTo($console);
        },
        reply = function reply(text) {
            $('<pre>')
                .text(text)
                .appendTo($console);
        };

    // Focus prompt on load
    $(document).ready(function () {
        $prompt.focus();
    });

    // Add a submit handler
    $('.prompt form').submit(function () {
        var $indicator = $('.prompt label'),
            chars = '|/-\\',
            index = 0,
            requestFinished = false,
            time = 0,
            loader = setInterval(function () {
                $indicator.text(chars[index]);

                index = (index + 1) % chars.length;

                if (requestFinished === true) {
                    $indicator.html('&gt;');
                    clearInterval(loader);
                }
            }, 200);

        command($prompt.val());

        $.ajax({
            url: '/controller/',
            type: 'POST',
            data: JSON.stringify({'command': $prompt.val()}),
            contentType: 'application/json',
            dataType: 'json'
        }).done(function(data){
            if(data.hasOwnProperty("console")) {
                reply(data.console);
                requestFinished = true;
            }

            $prompt.val('');
            $scroll.get(0).scrollTop = $scroll.get(0).scrollHeight;
        });

        return false;
    });
    // Show help
    $('.prompt a').on('click', function () {
        command('help');

        $.ajax({
            url: '/controller/',
            type: 'POST',
            data: JSON.stringify({'command': 'help'}),
            contentType: 'application/json',
            dataType: 'json'
        }).done(function(data){
            if(data.hasOwnProperty("console")) {
                reply(data.console);
                requestFinished = true;
            }
        });
    });
}(window, jQuery));
