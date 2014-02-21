# Logging Heroku Deployments in TraceView

To help understand the correlation between system events and performance trends,
TraceView provides the ability to log arbitrary events using it's
[Annotations API][2]. In this tutorial, we will demonstrate how we can leverage
Heroku's [Deploy Hooks][3] add-on to automatically log deployment annotations
in TraceView every time you push new code to Heroku.

**NOTE**: This tutorial assumes that you are:

- Using [TraceView on Heroku][5]
- Have the [Heroku CLI][8] installed

To begin, you're going to need your **TraceView Access** (API) key. Grab this
by navigating to the **Organization Overview** page (in the TraceView navigation
menu: `Settings => Overview`). Please note that you **must** be a TraceView
administrator to access this page in the application.

Next, let's navigate to where our Heroku application repository lives on our
local file system. For this example we'll be using [MegaURL][13], an URL
amplifier:

```bash
$ cd /home/dan/dev/megaurl
```

From here, we can use the `heroku` CLI tool to provision the Deploy Hooks
add-on:


```bash
$ heroku addons:add deployhooks:http \
--url="https://herokuapp1234567.tv.appneta.com/api-v2/log_message\
?key=abcd1234-ab12-ab12-ab12-abcefg123456\
&message=Deploy%20{{head}}\
&username={{user}}"
```

Some important notes when constructing the `--url` parameter:

- Replace `herokuapp1234567` with your TraceView subdomain
- Replace the `key` value with your TraceView Access key
- Customize the `message` value to include more [Heroku variables][9]
- [URL encode][10] any whitespace in your `message`

Now let's create an [empty commit][6] and deploy to Heroku:

```bash
$ git commit --allow-empty -m "An empty commit"
$ git push heroku master
Fetching repository, done.
Counting objects: 1, done.
Writing objects: 100% (1/1), 189 bytes, done.
Total 1 (delta 0), reused 0 (delta 0)

-----> Ruby app detected
...
-----> Launching... done, v57
-----> Deploy hooks scheduled, check output in your logs
       http://megaurl.herokuapp.com deployed to Heroku

To git@heroku.com:megaurl.git
   648ade2..beaa724  master -> master
```

At the end of the log, you can see that Heroku has scheduled the the deploy
hook. Thus, deployment annotations will now appear at the top of *all* your
TraceView application performance visualizations:

![a wild annotation appears][11]

And just click on the annotation to toggle it:

![toggle annotation information][12]

Correlating application performance changes with deployments couldn't be easier.

[1]: http://www.appneta.com/blog/traceview-beta-heroku/
[2]: http://dev.appneta.com/docs/api-v2/annotations.html
[3]: https://addons.heroku.com/deployhooks
[4]: http://dev.appneta.com/docs/api-v2/
[5]: https://devcenter.heroku.com/articles/traceview
[6]: http://stackoverflow.com/a/12269801/246102
[7]: https://devcenter.heroku.com/articles/deploy-hooks
[8]: https://devcenter.heroku.com/articles/heroku-command
[9]: https://devcenter.heroku.com/articles/deploy-hooks#customizing-messages
[10]: http://en.wikipedia.org/wiki/Percent-encoding
[11]: https://raw2.github.com/danriti/moleskine/master/heroku-deploy-hook/images/annotation_hover.png
[12]: https://raw2.github.com/danriti/moleskine/master/heroku-deploy-hook/images/annotation_display.png
[13]: http://megaurl.co
