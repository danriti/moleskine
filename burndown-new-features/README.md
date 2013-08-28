# New Features in Burndown

![Logo][6]

A few months ago we [annouced][1] [Burndown][2], an open source web application for
tracking the progress of Github milestones. For those of you that missed out:

> Harnessing the power of the mighty [Github API][3], Burndown provides a dead
simple way to generate a [burndown chart][4] for any Github milestone. This is
helpful for tracking both progress and performance, as well as identifying what
work remains.

Well we're happy to let you know that we've been hard at work adding some new
features and bug fixes to Burndown!

## 30 Day Summary

You can now view a "30 Day Summary", which provides a high level overview of
your repository. This chart tracks the number of issues that have been
opened and closed over the past 30 days, regardless of milestone. This is
useful in determining if your team is making positive traction
(i.e. `closed issues > opened issues`), especially when it seems like the
number of issues in your repository never drops.

![30 Day Summary][7]

As you can see in the screenshot above, [Bootstrap][8] is [on fire][9] with
over 1300+ issues (this includes pull requests) closed over the past 30 days!

## Filter Milestone Issues by Label

Milestone issue lists are now filterable by **label**, which you'll find along
the left-hand side of your issue lists. This is a helpful feature if you use
labels on Github to tag issues for team specific actions (i.e. QA, Test, etc).

![Filter by Label][10]

## Milestone Enhancements

Finally, we added some nice UI enhancements to our milestone view:

- List
- of
- Enhancements

Got an idea for a new feature? Do you use Burndown to help keep your team on
track? We'd be happy to hear your ideas or how you use Burndown, so feel free
to drop us a comment or [create an issue][5]!

[1]: http://www.appneta.com/blog/burndown-before-you-burn-out/
[2]: http://burndown.io
[3]: http://developer.github.com/v3/
[4]: http://en.wikipedia.org/wiki/Burn_down_chart
[5]: https://github.com/appneta/burndown/issues/new
[6]: https://raw.github.com/danriti/moleskine/master/burndown-new-features/images/logo.png
[7]: https://raw.github.com/danriti/moleskine/master/burndown-new-features/images/30_day_summary.png
[8]: https://github.com/twbs/bootstrap
[9]: http://www.youtube.com/watch?v=X7dFMbubxr4
[10]: https://raw.github.com/danriti/moleskine/master/burndown-new-features/images/filter_by_label.png
