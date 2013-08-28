# TBone Counter Example

## Welcome

Hey! I'm Dan Riti, the latest addition to the TraceView team! I
recently joined as a full stack engineer in the Providence office and it's been
an exciting past couple of weeks learning about the world of tracing distributed
web applications.

## TraceView

I've been working primarily on improving our Trace Details page, which provides
an in-depth look into the performance of individual requests. The
major challenge in our front end web application is managing data dependencies (i.e. Update `foo` when `bar` changes) while
also maintaining a rich user experience. We deal with a lot of data, from numerous sources,
and all with unique dependencies. Thus, we have developed [TBone](http://tbonejs.org/), an open-source
extension to [Backbone.js](http://backbonejs.org/) to help us out.

## Enter TBone

TBone removes the complexity of manually managing data dependencies in Backbone,
enabling "live" templates as well as functions that automatically re-execute when
the data they reference changes.

It's designed to build on top of existing backbone-powered apps and scale with
the application, enabling simple re-use of data
throughout your application without the need to tell the page what to update
when that data changes.

At AppNeta, we've used TBone to eliminate a set of custom page events
corresponding to interactions like "refresh data" and "add filter"; with a large application,
it becomes difficult to manage what exactly needs to be refreshed when something
changes. While Backbone is a critical step toward reducing this complexity,
TBone enables us to do so without even thinking about event binding; every view
and model stays in sync by design and without unnecessary work.

## Digging into TBone

Let's implement a sample application that demonstrates some of the "automagic"
of TBone. For this example, we will build a simple `counter` that increments
every second, implement some simple controls (Start/Stop/Reset), and finally demonstrate data
dependency by introducing a model that depends on the `counter`.

* Try out this example on [JS Bin](http://jsbin.com/uxuxew/10/edit)!
* Or view the code on [Github](https://github.com/danriti/tbone-counter-example).
* Or clone the repo: `git clone git://github.com/danriti/tbone-counter-example.git`

Now that you're looking at the code, let's get started!

First, we will create a model to represent the `counter` using TBone:

```javascript
tbone.createModel('counter').singleton();
```

Our `counter` model needs two attributes, `intervalId` and `value`.
We will be using the [setInterval](https://developer.mozilla.org/en-US/docs/DOM/window.setInterval) method to increment the counter, so `intervalId`
will store the interval id and `value` will simply store the counter value. So
let's set them:

```javascript
tbone.set('counter', {
    intervalId: 0,
    value: 0
});
```

Next, we will create a view for controlling (Start, Stop, Reset) the counter:

```javascript
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
```

Finally, we will bind our model and views to our template:

```html
<div class="container">
  <h1>TBone Counter Example!</h1>
  <hr>
  <div tbone="inline counter">
      <h3>Counter - <%=counter.value%></h3>
  </div>
  <div tbone="view counterControl">
      <button class="btn" id="start">Start</button>
      <button class="btn" id="stop">Stop</button>
      <button class="btn" id="reset">Reset</button>
  </div>
</div>
```

So what's happening? When you click the **Start** button, the `value` attribute in the
`counter` model is being incremented every second. Everytime the  model changes,
the template is forced to update to display the latest data. As you play with
the other controls, you will notice that template responds accordingly. This is
an example of "live" templating in TBone.

So now let's make things interesting. Let's introduce a new model called `timer`, however let's
assume it is depends on the `counter` model to keep track of time.  In TBone,
this is pretty simple:

```javascript
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
```

When creating the `timer` model, we tell TBone that this model depends on the
`counter` model by performing a `tbone.lookup` within the anonymous function we pass in. TBone
now knows a dependency exists between the two models and handles all the
heavy lifting for us. Thus, anytime the `counter` model changes, the
anonymous function will execute and the `timer` model attributes (seconds &
minutes) will be recalculated. Pretty neat, huh? Well, let's see it in action!

Just update your template to add the timer:

```html
<div tbone="inline timer">
    <h3>Timer (MM:SS) - <%=timer.minutes%>:<%=timer.seconds%></h3>
</div>
```

Now the newly created `timer` model will update seemlessly as the `counter`
model increments away!

Isn't TBone delicious? If you'd like seconds, be sure to [check it out on Github](https://github.com/appneta/tbone).
