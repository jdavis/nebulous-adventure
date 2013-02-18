'use strict';

/* Nebulous Adventure */


var app = app||(function (root, $) {
    var url_by_command = {'new':'/new/',
                          'resume':'/resume/'};

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


        var user_input = $prompt.val().split(' ');
        var user_command = user_input.shift();
        var user_arguments = user_input.join(' ');


        command($prompt.val());
        $prompt.val('');
        $console.get(0).scrollTop = $console.get(0).scrollHeight;

        if (user_command in url_by_command)
        {
            $.ajax({
                type: "GET",
                dataType: 'json',
                data: {'args':user_arguments},
                url: url_by_command[user_command]
            }).done(function(data){
                if(data.hasOwnProperty("console"))
                {
                    command(data.console);
                }
                if(data.hasOwnProperty("new_commands"))
                {
                    url_by_command = data.new_commands;
                }
            });
        }
        else
        {
            command('command not recognized');
        }


        return false;
    });
    // Show help
    $('.prompt a').on('click', function () {   

        alert('Eventually a help will show up here. ;)');
    });
}(window, jQuery));
