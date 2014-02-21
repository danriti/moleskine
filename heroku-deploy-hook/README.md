# Heroku Deploy Hook

This article is a brief tutorial on leveraging Heroku's [Deploy Hooks][3]
add-on to create deployment annotations in TraceView.

**NOTE**: This tutorial assumes that:

- You are already using [TraceView on Heroku][5]
- You have the [Heroku CLI][8] installed

To help understand the correlation between system events and performance trends,
TraceView provides the ability to log arbitrary events using the
[Annotations API][2]. In this tutorial, we're going to focus on using the
Annotations API to log code deployments/releases.

To begin, you're going to need your **TraceView Access** (API) key. Grab this
by navigating to the *Organization Overview* page (in the TraceView navigation
menu: Settings -> Overview). Please note that you *must* be a TraceView
administrator to access this page in the application.

Next, let's navigate to where our Heroku application repository lives on our
local file system:

```bash
cd /home/dan/dev/megaurl
```

From here, we can use the `heroku` CLI tool to provision the Deploy Hooks
add-on:


```bash
heroku addons:add deployhooks:http\
--url="https://herokuapp1234567.tv.appneta.com/api-v2/log_message\
?key=abcd1234-ab12-ab12-ab12-abcefg123456\
&message=Deploy%20{{head}}\
&username={{user}}"
```

Make sure you **update** the:

- TraceView subdomain
- The `key` parameter to match your *TraceView Access* key

```bash
git commit --allow-empty -m "An empty commit"
```

```bash
-----> Launching... done, v57
-----> Deploy hooks scheduled, check output in your logs
       http://megaurl.herokuapp.com deployed to Heroku

To git@heroku.com:megaurl.git
   648ade2..beaa724  foo -> master
```

[1]: http://www.appneta.com/blog/traceview-beta-heroku/
[2]: http://dev.appneta.com/docs/api-v2/annotations.html
[3]: https://addons.heroku.com/deployhooks
[4]: http://dev.appneta.com/docs/api-v2/
[5]: https://devcenter.heroku.com/articles/traceview
[6]: http://stackoverflow.com/a/12269801/246102
[7]: https://devcenter.heroku.com/articles/deploy-hooks
[8]: https://devcenter.heroku.com/articles/heroku-command
