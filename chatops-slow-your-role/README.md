# Slow Your Role: ChatOps Access Control

[ChatOps][7] is a growing trend in the DevOps world, where one can monitor and
control infrastructure and operations from the convenience of a chat room.
From building [Jenkins jobs][1] to executing [Fabric tasks][2], the
possibilities are endless thanks to [Hubot][3] and it's constantly growing
[plugin][5] [ecosystem][4].

One of the controversial tenets of ChatOps is the idea that *everyone* within
the chat room has the ability to run commands. This idea is built upon the
notion that team members understand they are accountable for their actions and
that all commands executed are visible to all team members within the chat room.
So not only do you have a "public" record what commands team members are
executing, but you also get real-time peer review.

While this rather open access philosophy leaves plenty of room for debate, it's
clear that it goes completely against the traditional view that only an
[elite few][6] have access to the critical components of a system. Thus, this
has the unfortunately consequence of making ChatOps hard (or even impossible)
for many to adopt within their organizations.

Enter [hubot-auth][8]. A Hubot plugin that makes assigning and enforcing
user-based roles easy as Sunday morning. That's right control freaks, rejoice!
You can finally convince your boss it's time to take operations to the next
level!

## Fall In

Getting started with `hubot-auth` is ~~easy~~ slightly complicated. The bad news
is that there are multiple versions of this plugin coexisting within the Hubot
community. The good news is that all but one are [unofficially deprecated][9],
so you just have to do a little cleanup before getting started:

1. Remove any reference to `auth.coffee` from your `hubot-scripts.json` file
2. Delete `auth.coffee` if it exists in the `scripts` directory within your
   Hubot directory

Now that you've removed any possibility of loading a deprecated version of the
plugin, let's go ahead and install the correct one:

```bash
$ npm install hubot-auth --save
```

Now add hubot-auth to your `external-scripts.json` file:

```json
["hubot-auth"]
```

Finally, set the [`HUBOT_AUTH_ADMIN`][10] environment variable to a comma
separated list of user IDs who should have admin privileges. Getting user IDs
is quite simple using the `redis-cli` command (assuming you're using redis to
store your Hubot brain):

```bash
$ redis-cli get "hubot:storage" | jsonlint | grep "Dan Riti" -C 3
    "12345": {
      "id": "12345",
      "jid": "12345@chat.example.com",
      "name": "Dan Riti",
      "mention_name": "Riti",
      "room": "traceview",
    }
$ redis-cli get "hubot:storage" | jsonlint | grep "Jane Doe" -C 3
    "54321": {
      "id": "54321",
      "jid": "54321@chat.example.com",
      "name": "Jane Doe",
      "mention_name": "Doe",
      "room": "traceview",
    }
$ export HUBOT_AUTH_ADMIN=12345,54321
```

And with a simple restart of Hubot, our `hubot-auth` plugin is setup and ready
to go!

## The Power Is Yours

Now that we've declared our admin users, we're ready to start dishing out
user roles. Like many other aspects of Hubot, the commands are simple and easy
to remember:

Adding a role:

```
Dan Riti> hubot Dan Riti has deploy role
Hubot> @Riti: OK, Dan Riti has the 'deploy' role.
```

Checking a specific user's current roles:

```
Dan Riti> hubot what roles does Dan Riti have
Hubot> @Riti: Dan Riti has the following roles: admin, deploy.
```

Removing a role from a user:

```
Dan Riti> hubot Dan Riti doesn't have deploy role
Hubot> @Riti: OK, Dan Riti doesn't have the 'deploy' role.
```

Now we're ready to lay down the law.

## I AM THE LAW

The last step of the process is actually enforcing user roles within your
Hubot scripts. `hubot-auth` exposes the following method on the `robot` object
for checking user roles:

```javascript
robot.auth.hasRole(msg.envelope.user,'<role>')
```

For a quick demonstration, let's look at how we can add role based access
control to the "Hello World" of Hubot, [`hubot ping`][11]:

```coffeescript
# Description:
#   Utility commands surrounding Hubot uptime.
#
# Commands:
#   hubot ping - Reply with pong

module.exports = (robot) ->
  robot.respond /PING$/i, (msg) ->
    msg.send "PONG"
```

A user enters: `hubot ping` and Hubot responds with `PONG`. Pretty simple stuff!
Now let's go ahead and update this script to only allow users with the `ping`
role from executing the command:


```coffeescript
# Description:
#   Utility commands surrounding Hubot uptime.
#
# Commands:
#   hubot ping - Reply with pong

module.exports = (robot) ->
  robot.respond /PING$/i, (msg) ->
    role = 'ping'
    unless robot.auth.hasRole(msg.envelope.user, role)
      msg.send "Access denied. You must have this role to use this command: #{role}"
      return
    msg.send "PONG"
```

And now let's see it in action:

```
Dan Riti> hubot ping
Hubot> Access denied. You must have this role to use this command: ping
Dan Riti> hubot Dan Riti has ping role
Hubot> @Riti: OK, Dan Riti has the 'ping' role.
Dan Riti> hubot ping
Hubot> PONG
```

Victory!

## Conclusion

- Updating scripts to respect roles
- Call to action to support plugin

[1]: https://github.com/github/hubot-scripts/blob/master/src/scripts/jenkins.coffee
[2]: https://github.com/appneta/hubot-fabric
[3]: https://hubot.github.com/
[4]: https://www.npmjs.org/search?q=hubot
[5]: https://github.com/hubot-scripts
[6]: http://en.wikipedia.org/wiki/Bastard_Operator_From_Hell
[7]: https://speakerdeck.com/jnewland/chatops-at-github
[8]: https://github.com/hubot-scripts/hubot-auth
[9]: https://github.com/github/hubot/pull/656
[10]: https://github.com/hubot-scripts/hubot-auth/blob/6b0165b94b5f99067199aadee3c7b6a710fde323/src/auth.coffee#L5
[11]: https://github.com/github/hubot/blob/5c655d24e3198db9fd8c49724271d2df6d34df7d/src/scripts/ping.coffee#L11-L12
