# Slow Your Role: ChatOps Access Control

[ChatOps][7] is a growing trend in the DevOps world, where one can monitor and
control infrastructure and operations from the convenience of a chat room.
From building [Jenkins jobs][1] to executing [Fabric tasks][2], the
possibilities are endless thanks to [Hubot][3] and it's constantly growing
[plugin][5] [ecosystem][4].

One of the controversial tenets of ChatOps is the idea that *everyone* within the
chat room has the ability to run commands. While one could argue about the pros
and cons to this rather open philosophy, it goes completely against the
traditional approach that only an [elite few][6] have access to the critical
components of a system. Thus, this fact has the unfortunate consequence of making
ChatOps hard (or even impossible) to adopt within many organizations.

[1]: https://github.com/github/hubot-scripts/blob/master/src/scripts/jenkins.coffee
[2]: https://github.com/appneta/hubot-fabric
[3]: https://hubot.github.com/
[4]: https://www.npmjs.org/search?q=hubot
[5]: https://github.com/hubot-scripts
[6]: http://en.wikipedia.org/wiki/Bastard_Operator_From_Hell
[7]: https://speakerdeck.com/jnewland/chatops-at-github
