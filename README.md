#[Shortcircuits.io](http://shortcircuits.io)

Content for my website. 
## Installation
1. `pip install -r requirements.txt`
2. Install jpegtran and optipng libraries for asset managament
3. Get the theme from [my-theme](https://github.com/nikhilkalige/mytheme)


- The raw content is in **develop** branch and **master** holds the generated content
- To publish a new article, checkout develop branch and then run `make html` to generate it. 
- Run `./merge.sh "Commit message"`. This will checkout the master branch and copy the content of output folder and commits it to the master. 