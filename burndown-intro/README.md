# Burndown Before You Burn Out

![Logo](https://raw.github.com/danriti/moleskine/master/burndown-intro/images/logo.png)

At Appneta we use an extremely lightweight method to develop software.  While it
doesn't necessarily map exactly onto one of the [many][1] [agile][2] [methodologies][3],
our process is very much inspired by [this video][4].

Although there are many unique characteristics for each software development
methodology, one thing is consistent: the goal of **progress**.  Everyone wants to
know how a particular project or task is coming along and when it's going to be
complete. So even if you don't believe in due dates and delivering to a
schedule, it's still useful to know and be able to communicate to
others your current progress.

To aid us on our never-ending quest to know just how awesome we really are,
we've developed [Burndown][5], an open source tool to assist
in tracking progress of a Github milestone!

Github is great for source and issue management, but it's a bit lacking for
project management. One thing we found ourselves wanting was a burndown chart
to help keep track of progress and Burndown made it easy to make sure momentum
didn't die on our projects. Harnessing the power of the mighty [Github API][6],
Burndown provides a dead simple way to generate a [burndown chart][7] for any
Github milestone. This is helpful for tracking both progress and performance,
as well as identifying what work remains.

![Progress](https://raw.github.com/danriti/moleskine/master/burndown-intro/master/images/good_burndown.png)

Example of a burndown chart for [appneta/burndown][13]. The chart displays
created issues versus time, actual work complete
(`total_issues - closed_issues`) versus time, as well as an ideal line to help
keep pace.

![Issues](https://raw.github.com/danriti/moleskine/master/burndown-intro/master/images/issues.png)

We also display the open and closed issues associated with the milestone, along
with the gravatars of the issue creator (left) and the issue assignee (right).

Burndown is built on top of [rails-github-skeleton][8],
which makes authenticating with the Github API easy as pie (thanks to
[Omniauth][9]). Finally, the front-end is built with both [Backbone][10] and
[Rickshaw][11], because Javascript MVCs and d3 libraries are all the rage these
days.

Burndown is open source, so feel free to use it anywhere you'd like or use our
free hosted version over at [burndown.io][5].

Got feature ideas? Feel free to add an [issue][12] or send us a pull request! So
what are you waiting for? Jump right in and start burning down today!

[1]: http://en.wikipedia.org/wiki/Scrum_(development)
[2]: http://en.wikipedia.org/wiki/Kanban_(development)
[3]: http://en.wikipedia.org/wiki/Extreme_Programming
[4]: http://zachholman.com/talk/how-github-uses-github-to-build-github/
[5]: http://burndown.io
[6]: http://developer.github.com/v3/
[7]: http://en.wikipedia.org/wiki/Burn_down_chart
[8]: https://github.com/danriti/rails-github-skeleton
[9]: http://www.omniauth.org/
[10]: http://backbonejs.org/
[11]: http://code.shutterstock.com/rickshaw/
[12]: https://github.com/appneta/burndown/issues
[13]: https://github.com/appneta/burndown/issues?milestone=1&page=1&state=open
