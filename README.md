# MRtrix website

This is the repository that holds the content for the MRtrix website (http://www.mrtrix.org/). Using GitHub pages, commits to this repository will automatically rebuild the final statically generated html pages. If you're interested in more information, check out the guide [here](https://pages.github.com/).

## For content contributors : Static data

Most of the static information (e.g. frontpage material) is located in the `_data` directory. In particular, most of the files within are stored as [YAML](http://www.yaml.org/) (.yml) files which, quoting the yaml page, "is a human friendly data serialization standard for all programming languages." For example, looking at `_data/social-media.yml`

```
- name: Google+
  icon: fa fa-google-plus-square
  link: https://plus.google.com/communities/111072048088633408015

- name: GitHub
  icon: fa fa-github-square
  link: https://github.com/MRtrix3/mrtrix3
```

In this case, we have a list of dictionaries with key values `name,icon,link`. Note, how `-` denotes the start of a new list element. Also, keep in mind that *indentation matters*, so be wary of this as you make changes.

### Adding author information: _data/authors.yml

Please add an entry in this file to link between your name and github account (along with other metadata). Sample entry

```
- name: Joe Smoe
  nickname: Joey
  github: jsmoe
  twitter: jsmoe12
  website: http://academicwebsite.org
```
* `name`: Self-explanatory
* `nickname`: The name that will appear underneath your image in a blog post. For layout reasons, try to keep this to a single name.
* `github`: Your github handle. *You will need set this in order to post a blog entry*
* `twitter`: (Optional) Your twitter handle. This meta data will appear underneath your image in a blog post.
* `website`: (Optional) A link to your academic website (or other). This meta data will appear underneath your image in a blog post.

### Frontpage: _data/frontpage/banner.yml

Content that appears in banner on front-page.

* `buttons`: List of buttons to embed inside banner

### Frontpage: _data/frontpage/about.yml

An about section that appears just below the frontpage banner.

* `title`: Header of section
* `description`: The actual text. Note that yaml allows you to separate the string over multiple lines. e.g.

```
description: | # The vertial dash allows you to use an indented multi-line string
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
    quis nosrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
```

### Frontpage: _data/frontpage/features.yml

The collection of features that are displayed in an image carousel

* `title`: Name of feature
* `description`: A brief description. Again, you can separate this over multiple lines as shown in the About section. *Note* Try to keep this to about one sentence. Otherwise, the text may flow over the image.
* `image`: The feature image location *relative to the base directory*. e.g.

```
image: /images/frontpage/feature.jpeg
```

* *Note* For consistency, please store the feature images in `images/frontpage`.
* *Note* Additionally, the image dimensions should also be consistent. I think something like 750x400 would work well, but feel free to specify something larger, just as long as all images have the same size.


### Frontpage: _data/frontpage/contributors.json

The metadata for the list of github MRtrix contributors. This data is a simple copy and paste of the GitHub API request:

```
https://api.github.com/repos/MRtrix3/mrtrix3/contributors
```

GitHub places restrictions on the number of fetch requests, so it's much safer (and faster) to simply store this request statically.

* *Note* In the future, if the size of the contributor list grows we will need to update this file.

### Frontpage: _data/frontpage/affiliations.yml

Specifies the list of affiliated institutions that will appear at the bottom of the frontpage.

* `name`: Name of affiliation
* `link`: A href link to the affiliation's website
* `logo`: The logo image location *relative to the base directory* e.g.

```
logo: images/affiliations/logo.jpg
```

* *Note* For consistency, please store the affiliation images in `images/affiliations`.
* *Note* While the affiliation image dimensions *don't* need to be consistent, please ensure that they're somewhat sizeable as the layout/size of the rendered image can alter depending on whether viewing the site on a desktop or mobile device. In general, I think a width/height of at least 300px should be fine.


### For content contributors : Publication data (_data/publications.yml)

The list of publication data that is fetched from the mrtrix source. In particular, in `_data_scripts/` there is a Python script `mrtrix_publications_crawler.py` that will parse the mrtrix command files looking for references and then output a yml formatted list of publications. e.g.

```
./mrtrix_publications_crawler.py --commands_dir ~/mrtrix/cmd --output_path ../_data/publications.yml
```

There are some assumptions that the script makes in order to sucessfully parse the command source

1. All reference are wedged between a `REFERENCES` block ending with a semi-colon. Each reference is denoted by '+'
2. The reference block must be immediately before the `ARGUMENTS` block
3. Ordering of reference information is author, title and then journal details (journal name, year etc.)
4. For journal details, the year must come immediately after the journal title (e.g. `NeuroImage, 2012`)
5. Any additional information such as the option/setting that is specific to the reference is stated prior to listing the author and begins with the character '*'
6. *Note* As we want to differentiate between internal and external publications, you can denote the former by including the inline comment `// Internal` at the end of the author listing.

Sample excerpt

```
  REFERENCES
    + "Smith, R. E.; Tournier, J.-D.; Calamante, F. & Connelly, A. " // Internal
      "Anatomically-constrained tractography:"
      "Improved diffusion MRI streamlines tractography through effective use of anatomical information. "
      "NeuroImage, 2012, 62, 1924-1938";

    + "* If using option --sample"
      "External, A. E.; External, B.; External C"
      "On sample data: A new beginning"
      "Nature, 2015, 62, 1924-1938";

  ARGUMENTS
    + Argument ("5tt_in",  "the input 5TT segmented anatomical image").type_image_in()
    + Argument ("mask_out", "the output mask image")                  .type_image_out();
```


## For content contributors : Writing posts

All blog posts are stored in `_posts` and can be written using markdown using the [kramdown syntax](http://kramdown.gettalong.org/syntax.html). However, posts follow strict rules regarding subdirectory location and naming convention. Additionally, there is some addtional metadata that needs to be incorporated at the start of your post. Hence, to make this a bit easier for bloggers, I've provided a companion script `newpost.py` at the top directory of the site that will correctly initialise a new post. e.g.

```
./newpost.py --title 'My awesome title' --author 'jdtournier' --categories 'featuer1 feature2'
```

* `title`: Title of blog post
* `author`: The github handle corresponding to the author
* `categories`: (Optional) A single string listing tags associated with post

Once run, a new markdown document will be created in the `_posts` directory. From there, open up the new document and add your markdown content. By default, there's sample content included that showcases a few of the markdown features such as highlighted code snippets and math blocks using LaTeX syntax.

Once you're happy with your new post, simply commit it to the repository and it should be added to the list of visible blog posts on the website.

## Problems / Suggestions ?

If you encounter any issues with the site or want to suggest any new website features please create a new GitHub issue. 














