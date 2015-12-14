# iron-chef

Chef is a configuration management tool.
Repeatability of environments.
Lots of outdated documentation.
Confusing and steep learning curve.
ChefDK attempts to solve this.

## Prerequisites

1. Virtualbox
2. Vagrant
3. ChefDK (Development Kit)

## Lets Go

```bash
$ chef generate repo instabox-chef
$ cd instabox-chef
$ chef generate cookbook cookbooks/traceview
$ cd cookbooks/traceview
```

Update `.kitchen.yml`.

```bash
$ kitchen create
```

Write a test.

```bash
$ kitchen verify
```

Test fails.

```bash
$ chef generate recipe user
$ chef generate attribute default
```

Create tests. Test. Fail. Implement recipe. Test. Pass.
Refactor to use attribute. Test. Pass.


## Reference

- A **role** in Chef is a categorization that describes what a specific machine
  is supposed to do.
- An **environment** is simply a designation meant to help an administrator know
  what stage of the production process a server is a part of.


[1]: https://docs.chef.io/install_dk.html
[2]: https://github.com/berkshelf/berkshelf/issues/378#issuecomment-13842960
