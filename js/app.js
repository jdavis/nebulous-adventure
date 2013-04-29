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
                }, 200);

            if (!hide) {
                $('<pre>')
                    .text('> ' + text)
                    .appendTo($console);
            }

            if ($prompt.val() in localCommands) {
                localCommands[text]();
                requestFinished = true;
                resetPrompt();
            } else {
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
                    resetPrompt();
                });
            }

            return false;
        },
        reply = function (text) {
            $('<pre>')
                .text(text)
                .appendTo($console);
        },
        resetPrompt = function () {
            $prompt.val('');
            $scroll.get(0).scrollTop = $scroll.get(0).scrollHeight;
        },
        clearConsole = function () {
            $console.html('');
        },
        localCommands = {
            'clear': clearConsole,
        };

    // Focus prompt on load
    $(document).ready(function () {
        $prompt.focus();
        command('status', true);
    });

    // Add a submit handler
    $('.prompt form').submit(function () {
        command($prompt.val());
        return false;
    });

    // Show help
    $('.prompt a').on('click', function () {
        command('help');
    });
}(window, jQuery));
