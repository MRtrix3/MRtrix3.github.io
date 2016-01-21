# MRtrix website

This is the repository that holds the content for the MRtrix website (http://www.mrtrix.org/). Using GitHub pages, commits to this repository will automatically rebuild the final statically generated html pages. If you're interested in more information, check out the guide [here](https://pages.github.com/).

## For content contributors : Static data

Most of the static information (e.g. frontpage material) can be located in the `_data` directory. In particular, most of the files within are stored as [YAML](http://www.yaml.org/) (.yml) files which, quoting the yaml page, "is a human friendly data serialization standard for all programming languages." For example, looking at `_data/social-media.yml`

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

Please add an entry to this file to link between your name and github account (along with other metadata). Sample entry

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

* `description`: A slogan that appears inside banner. Try to keep this short. There's a separate about section (see about.yml) that can elaborate on the product description.
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

The list of publication data


## For content contributors : Writing posts










