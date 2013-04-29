'use strict';

/* Nebulous Adventure */


(function (root, $) {
    var $console = $('.console div.content'),
        $scroll = $('.console'),
        $prompt = $('#prompt'),
        command = function (text, hide) {
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
                }, 200),
                parts = text.split(' '),
                cmd = parts[0];

            if (!hide) {
                $('<pre>')
                    .text('> ' + text)
                    .appendTo($console);
            }

            console.log('Command = ' + cmd);

            if (cmd in localCommands) {
                var stop = localCommands[cmd]();
                requestFinished = true;
                if (stop) return;
            }

            $.ajax({
                url: '/controller/',
                type: 'POST',
                data: JSON.stringify({'command': text}),
                contentType: 'application/json',
                dataType: 'json'
            }).done(function(data){
                if(data.hasOwnProperty('console')) {
                    reply(data.console);
                    requestFinished = true;
                }
            });
        },
        reply = function (text) {
            $('<pre>')
                .text(text)
                .appendTo($console);
            scrollConsole();
        },
        scrollConsole = function () {
            $scroll.get(0).scrollTop = $scroll.get(0).scrollHeight;
        },
        resetPrompt = function () {
            $prompt.val('');
            scrollConsole();
        },
        clearCommand = function () {
            $console.html('');
            return true;
        },
        startCommand = function () {
            clearCommand();
        },
        localCommands = {
            'clear': clearCommand,
        };

    // Focus prompt on load
    $(document).ready(function () {
        $prompt.focus();
        command('status', true);
    });

    $(window).on('beforeunload', function () {
        return 'Leaving Nebulous Adventure will cause you to lose all your unsaved progress.'
    });

    // Add a submit handler
    $('.prompt form').submit(function () {
        var val = $prompt.val();
        resetPrompt();
        command(val);
        return false;
    });

    // Show help
    $('.prompt a').on('click', function () {
        command('help');
    });
}(window, jQuery));
