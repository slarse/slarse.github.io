Title: Projects

I always have a few side projects going. The one I'm currently most invested in
is RepoBee.

## RepoBee
RepoBee is a tool for managing Git repositories on GitHub for education. It can
do things like generate repositories for students, clone student repositories
in batches, run tasks on the cloned repositories as defined by plugins, and
more. I'm really quite proud of it, and have some exciting things coming up for
it this summer (that I can't yet talk about).

* [RepoBee's website](https://repobee.org)
* [RepoBee on GitHub](https://github.com/repobee/repobee)
* [RepoBee's documentation](https://repobee.readthedocs.io)

## Labelbot
Labelbot is a small GitHub bot that I developed with a classmate for a course
on [DevOps and Automated Testing](https://github.com/kth/devops-course). A
problem that occured during the course was that students, who only had read
access to the course repository, couldn't label issues with labels such as
`collaboration_wanted` or `question`. The idea of Labelbot is to allow any user
with read access to label an issue through markup in an issue body, that is
then checked against a list of allowed labels. If a requested label is allowed,
Labelbot will set it on the issue on behalf of the requester, which hopefully
reduces the effort of repository maintainers in keeping issues properly
categorized. The video below shows a small example of this.

<img alt="Labelbot example" src="https://raw.githubusercontent.com/slarse/labelbot/master/images/labeling.gif" width="90%">

It incorporates a lot of fun technologies, such as continuos integration, 
continuous deployment to AWS Lambda as well as interaction with the GitHub API
using secure tokens. It's usable as is, but is more a proof-of-concept than
anything else, and it is unlikely that we will keep developing it.

* [Labelbot on GitHub](https://github.com/slarse/labelbot)
* [Labelbot's documentation](https://labelbot.readthedocs.io)

## clanimtk/clanim
`clanimtk` is a fun little framework that I developed a while back. It helps in
developing simple command line animations for programs with functionality that
take enought time for users to have to be reminded that the program is still
running. `clanim` is a library that contains some example animations created
with `clanimtk`. Below is one of the more advanced animations I created.

<img alt="clanimtk example" src="https://raw.githubusercontent.com/slarse/clanimtk/master/docs/images/hello_world.gif" width="90%">

I never got as far with it as I would have liked, but what's there is still
usable and required some non-trivial use of some of Python's awesome language
features.

* [`clanimtk` on GitHub](https://github.com/slarse/clanimtk)
* [`clanim` on GitHub](https://github.com/slarse/clanim)
