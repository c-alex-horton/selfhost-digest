# Selfhost Digest
A simple python script to fetch posts from Lemmy (and soon more) and output them in a formatted MarkDown file for easy reading. Fight the morning doom-scroll and instead limit your news intake. 

## Install and Run

Clone the Repo and enter the selfhost-digest directory
`git clone https://github.com/c-alex-horton/selfhost-digest.git && cd selfhost-digest/`

Install the packages
`make install`

Run with make
`make run`

By default, you're output will be in `selfhosted-digest/export/`

## Config.yml
```
---
# If true, runs in testing mode. Will only download articles once if a posts_output.json does not exist.
testing: false

# Ensures every post has an image, using a placeholder where needed. Can improve readability.
image_for_all_posts: true

# Where to save the generated output
output_path: ./export/

# If left as "default", the User-Agent will appear as:
# 'Selfhost-Digest/1.0 <Your Network Host Name> https://github.com/c-alex-horton/selfhost-digest'
user_agent_name: default

modules:
  weather:
    location: Denver, Colorado

  lemmy:
    instances:
      - url: https://lemmy.world
        communities:
          - name: news
            posts: 5
          - name: technology
            posts: 3
      - url: https://lemmy.ml
        communities:
          - name: linux
            posts: 2

```

## Placeholder.jpg
To change the placeholder image, simply replace `placeholder.jpg` with whatever jpg you like.


Placeholder image from [Pixabay](https://pixabay.com/illustrations/newspaper-article-journal-headlines-3324168/)