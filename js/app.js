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
                cmd = parts[0],
                gameKey = $('body').data('gameKey');

            if (!hide) {
                $('<pre>')
                    .text('> ' + text)
                    .appendTo($console);
            }

            if (cmd in localCommands) {
                var stop = localCommands[cmd]();
                requestFinished = true;
                if (stop) return;
            }

            $.ajax({
                url: '/controller/',
                type: 'POST',
                data: JSON.stringify({'command': text, 'gameKey': gameKey}),
                contentType: 'application/json',
                dataType: 'json'
            }).done(function(data){
                if('console' in data) {
                    reply(data.console);
                }
                if ('callback' in data) {
                    var cb = data['callback']['name'],
                        args = data['callback']['args'];

                    if (cb in callbacks) {
                        callbacks[cb].apply(this, [].concat(args));
                    }
                }
                requestFinished = true;
            });
        },
        reply = function (text) {
            $('<pre>')
                .text(text)
                .appendTo($console);
            scrollConsole();
        },
        attachUnload = function () {
            $(window).on('beforeunload', function () {
                return 'Leaving Nebulous Adventure will cause you to lose all your unsaved progress.'
            });
        },
        removeUnload = function() {
            $(window).off('beforeunload');
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
        },
        gameKeyCallback = function (key) {
            console.log('GameKeyCallback');
            $('body').data('gameKey', key);
            console.log('Key = ' + key);
            attachUnload();
        },
        callbacks = {
            'gameKey': gameKeyCallback,
        };

    // Focus prompt on load
    $(document).ready(function () {
        $prompt.focus();
        command('status', true);
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
