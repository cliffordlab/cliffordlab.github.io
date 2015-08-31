# gdclifford.info

This is code for the Clifford Lab website.

We have a custom domain so cliffordlab.github.io redirects to gdclifford.info.

This site is built with [jekyll](http://jekyllrb.com/).  You must have ruby and ruby gems installed to generate and test the site.

```
gem install jekyll
```

```
jekyll serve
```

Navigate to `http://localhost:4000`.


###Directory Breakdown

####_data

YAML files that hold things such as lab member info.

####_includes

HTML templates for the header, footer, and large text blobs.

####_layouts

Holds `default.html` which ties everything together.

####_sass

Partials for sass.

####assets

Where CSS, JS, images are kept.  

`main.scss` is where all the partials are imported.

####Pages

Standalone HTML pages.













