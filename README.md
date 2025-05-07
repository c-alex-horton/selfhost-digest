# Selfhost Digest
A simple python script to fetch posts from Lemmy (and soon more) and output them in a formatted MarkDown file for easy reading. Fight the morning doom-scroll and instead limit your news intake. 

## Config.yml
```
---
# If true, run's in testing mode. Will only download articles once if it doesn't have a posts_output.json already. 
testing: false 

# Make sure every post has an image, using placeholder where needed. Can imporve readability
image_for_all_posts: true

# Where to save the output
output_path: ./export 


# Lemmy Instances & Communities to pull from
instances:
  - url: https://lemmy.world
    communities:
      - name: news # Community Name
        posts: 5 # Amount of posts to fetch
      - name: technology
        posts: 3
  - url: https://lemmy.ml
    communities:
      - name: linux
        posts: 2
```


Placeholder image from [Pixabay](https://pixabay.com/illustrations/newspaper-article-journal-headlines-3324168/)