'use strict';

/* Nebulous Adventure */


(function (root, $) {
    var $console = $('.console'),
        $prompt = $('#prompt'),
        command = function command(text) {
            $('<p>')
                .text('> ' + text)
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
            duration = 2000,
            interval = 200,
            time = 0,
            loader = setInterval(function () {
                $indicator.text(chars[index]);

                index = (index + 1) % chars.length;
                time += interval;

                if (time >= duration) {
                    $indicator.html('&gt;');
                    clearInterval(loader);
                }
            }, 200);

        command($prompt.val());
        $console.get(0).scrollTop = $console.get(0).scrollHeight;

        return false;
    });

    // Show help
    $('.prompt a').on('click', function () {
        alert('Eventually a help will show up here. ;)');
    });
}(window, jQuery));
