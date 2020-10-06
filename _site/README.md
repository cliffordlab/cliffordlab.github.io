![Fetal Monitor](assets/img/test.jpg)

# Welcome to the Clifford Lab Website!

This document will explain how to set up an environment for testing changes to the website before making them live, perform common updates and deploy the website.

---

# Setting Up Testing Environment

## ---!  BEFORE DOING ANYTHING - bmiwebdev !---

**If you do NOT want to set up a local testing environment for managing the website**, please contact the BMI administration to have them get you established with the bmiwebdev server. This server is ready to go with all necessary packages and environments - that way, you can easily log in and work on the website.

## bmiwebdev Tutorial

bmiwebdev does run Linux Fedora and for anyone not familiar with Linux, the following guide is provided to get you set up with testing changes locally before making changes live.

### Setting Up Git

If you do not have a [github account](https://github.com/), you will need to make one. Once you have made a github account, follow these steps:

1. Log into bmiwebdev
2. Press `ctrl + alt + t` to open the terminal
3. Enter the following `git --global user.name "[YOUR GITHUB USERNAME]"`
4. Enter the next line `git --global user.email [YOUR GITHUB EMAIL]` (no quotes around email!)
5. Clone your version of the lab website to the server using  `git clone https://github.com/cliffordlab/cliffordlab.github.io.git`

Now, you have the website code! The folder with the code will be named "cliffordlab.github.io".

> Note: You will need permission to the github repository for you to make changes to the live website. Speak with BMI administration or Dr. Clifford for access!

> Note: You will need to familiarize yourself with how Git works - there are plenty of tutorials and I would suggest the official tutorial from the [Git Website](git-scm.com).

### Running Jekyll

Jekyll is a program that is installed in bmiwebdev that allows you to preview changes you made to a website before making them live. The benefit of this is that you can preview **exactly** how the website will look when it is live and gives you the opportunity to catch any mistakes. Here is how to run Jekyll:

1. Log into bmiwebdev
2. Press `ctrl + alt + t` to open the terminal
3. Using the terminal, run `cd ~/cliffordlab.github.io`
4. Once there, run the command `jekyll serve`. You should receive an output where it shows a line like `Server address: http://localhost:4000`
5. Copy the localhost address and paste that into an internet browser

Now, you can peruse the local version of the website as if it is live! Any changes you make to the codebase while jekyll is still "serving" the website pages, will appear in localhost (you may need to refresh the page for the changes to show up).

> Note: Jekyll renders Markdown into HTML; the HTML is then stored in `_site/` files.

> Error Note: If jekyll does not work when you run `jekyll serve`, run this command in your terminal, `source ~/.rvm/bin/rvm`. This should now enable jekyll to work properly.

---

## Linux Set-Up

If you want to run jekyll and the website locally, it is fairly straight forward. For this tutorial, I am going to assume you are familiar with the major concepts with Linux (package managers, distributions, etc.) Instructions are below:

1. Install [RVM](https://rvm.io/rvm/install) to your system with the latest version of Ruby (the RVM instructions will tell you what to do)
2. Install [Jekyll](https://jekyllrb.com/docs/installation/) and make sure you have all the proper dependencies
3. Clone the [Clifford Lab](https://github.com/cliffordlab/cliffordlab.github.io) github repository to your machine
4. Go to the repository and run `jekyll serve`

From there, you should be set to go! Enjoying playing around with Jekyll locally.

---

## Windows and OS X

Uh... Use bmiwebdev! Speak with BMI administration to get it set up (look at instructions for bmiwebdev above)!

---

# Updating the Website

## _page_generators

In the _page_generators folder, there are tools provided for easy updating of critical parts of the website. These tools are designed to be sufficiently extensible for adding new components to a page. Please, do not hard code anything and reinvent the wheel. Here are descriptions of the current page generator tools:

### pub_page_generator.py

This is a simple Python script that enables you to update publications and render new HTML content. Let's walk through an example:

Say we have the journal publication "Doe, J. How to Be Awesome in 5 Steps. Nature. August 27;42(1) 2018." with the corresponding URL: "https://www.youtube.com/watch?v=VWf8CXwPoqI". We could render the HTML ourselves in the pages/publications.html but we have other things to do. Now, here is how to get the pub_page_generator.py to generate this journal entry for us:

1. Go to the publication_info folder and go into the data folder.
2. Open the JOURNALS.txt file.
3. Now before we take our journal publication and put it at the end of the file we have to format it properly. Here is how the format should look:
>Doe, J|How to Be Awesome in 5 Steps| Nature. August 27;42(1) 2018|https://www.youtube.com/watch?v=VWf8CXwPoqI
4. Now, take that formatted citation and put it at the end of the JOURNALS.txt **all on one line**. Make sure to save the file!
5. Run the pub_page_generator.py script with the command `python pub_page_generator.py`
6. Using Jekyll, you should now see a new entry in the Journal section of the publications page!

For different publication types either look for the corresponding file in the data folder or speak with Dr. Clifford to determine where it goes.

>Note: Keep in mind when you are adding new entries, you will need to put them manually in proper date order - check the publication dates in the previously recorded entries.

## How to Update Members Page

To update the members page, go to the file `members.yml` in the _data file. To add a new person to the members page, add new yml like so:

```
-
 name: Who, MD
 title: Time Lord
 dept: TARDIS
 location: Space
 picture: /assets/img/who.jpg
 twitter: "https://twitter.com/bbcdoctorwho"
 email: mailto:badwolf@infinitymail.xio
 site: "https://www.doctorwho.tv/"
 pubs: "http://www.bbc.com/"
-
```

Make sure if you want to include an image alongside a person's profile, to put that image in the _site/assets/img folder.

> Note: Do not forget the hyphens and indentation levels! yml files are quite picky.

## Updating the Rest of the Website

The rest of the website is much easier to update. Here are locations for files and what files to edit to get the desired changes:

+ Update Alumni or Gari's bio in `__people/__`
+ Update Info (onboarding) at `__info.md__`
+ Update Ethics at ` __ethics.md__`
+ Update Jobs Page at ` __jobs.md__`

---

# Notes

You may notice an .old_pages folder; these are where old pages from the website go - rather than delete those files, put them here and comment the permalink path out at the top of the old files.

<br/>

If you have any questions about things, contact the BMI administration or [TheCedarPrince](mailto:thecedarprince@gmail.com).

<br/>

~ TheCedarPrince
