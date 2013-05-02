'use strict';

/* Nebulous Adventure */


(function (root, $) {
    var $console = $('.console div.content'),
        $scroll = $('.console'),
        $prompt = $('.prompt'),
        $promptInput = $('#prompt'),
        $container = $('.container'),
        $body = $('body'),
        findCommands = function (text) {
            return text.replace(/`(.*)`/g, function (match, command) {
                return $('<div>').append($('<a>').addClass('command').attr('href', '#').text(command)).html();
            });
        },
        escape = function (text) {
            return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
        },
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
                tempKey = $('body').data('tempKey');

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
                data: JSON.stringify({'command': text, 'tempKey': tempKey}),
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
                $promptInput.focus();
            });
        },
        reply = function (text) {
            var filtered = findCommands(escape(text));
            $('<pre>')
                .html(filtered)
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
            $promptInput.val('');
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
        tempKeyCallback = function (key) {
            $('body').data('tempKey', key);
            attachUnload();
        },
        colorCallback = function (colors) {
            $body.css('backgroundColor', colors.body);
            $container.css('backgroundColor', colors.container);
            $prompt.css('backgroundColor', colors.container);
        },
        callbacks = {
            'tempKey': tempKeyCallback,
            'color': colorCallback,
        };

    // Focus prompt on load
    $(document).ready(function () {
        $promptInput.focus();
        command('welcome', true);
    });

    // Add a submit handler
    $('.prompt form').submit(function () {
        var val = $promptInput.val();
        resetPrompt();
        command(val);
        return false;
    });

    // Show help
    $('.prompt a').on('click', function () {
        command('help');
    });

    $('.console').on('click', 'a.command', function (e) {
        var $this = $(this);

        command($this.text());
        e.preventDefault();
    });
}(window, jQuery));
