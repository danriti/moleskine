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

Enter [hubot-auth-me][8]. A Hubot plugin that makes assigning and enforcing
user-based roles easy as Sunday morning. That's right control freaks, rejoice!
For now you can finally convince your boss it's time to take operations to the
next level!

## Next Witty Section Title

TBD.


[1]: https://github.com/github/hubot-scripts/blob/master/src/scripts/jenkins.coffee
[2]: https://github.com/appneta/hubot-fabric
[3]: https://hubot.github.com/
[4]: https://www.npmjs.org/search?q=hubot
[5]: https://github.com/hubot-scripts
[6]: http://en.wikipedia.org/wiki/Bastard_Operator_From_Hell
[7]: https://speakerdeck.com/jnewland/chatops-at-github
[8]: https://github.com/hubot-scripts/hubot-auth
