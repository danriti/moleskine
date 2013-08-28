// app.js

(function () {
    /**
     * Models
     */
    tbone.createModel('counter').singleton();
    tbone.set('counter', {
        intervalId: 0,
        value: 0
    });

    tbone.createModel('timer', function() {
        var count = tbone.lookup('counter.value') || 0;
        var rval = {};

        // Calculate seconds and minutes.
        var seconds = count % 60;
        var minutes = Math.floor(count / 60);

        // Pad the left side (i.e. 09 instead of 9) of the seconds
        // and minutes.
        rval.seconds = _.string.pad(seconds, 2, '0');
        rval.minutes = _.string.pad(minutes, 2, '0');

        return rval;
    }).singleton();

    /**
     * Views
     */
    tbone.createView('counterControl', function() {
        var self = this;

        var startBtn = self.$('button#start');
        var stopBtn = self.$('button#stop');
        var resetBtn = self.$('button#reset');

        // Initially disable the stop button.
        stopBtn.attr("disabled", true);

        // Event handler for the start button click.
        startBtn.click(function() {
            // Set button states.
            startBtn.attr('disabled', true);
            stopBtn.removeAttr('disabled');

            // Increment the counter every second.
            var intervalId = setInterval(function() {
                // Lookup the counter model value.
                var i = tbone.lookup('counter.value');

                // Increment the counter model value.
                tbone.set('counter.value', i+1);
            }, 1000);

            tbone.set('counter.intervalId', intervalId);
        });

        // Event handler for the stop button click.
        stopBtn.click(function() {
            // Set button states.
            stopBtn.attr('disabled', true);
            startBtn.removeAttr('disabled');

            // Fetch the interval id and stop incrementing the counter.
            var intervalId = tbone.lookup('counter.intervalId');
            clearInterval(intervalId);
        });

        // Event handler for the reset button click.
        resetBtn.click(function() {
            // Reset the counter value to 0.
            tbone.set('counter.value', 0);
        });
    });

    /**
     * TBone
     */
    tbone.render(jQuery('[tbone]'));
}());
