## [Lab Website](https://github.com/cliffordlab/cliffordlab.github.io) -

This document will explain where and how to perform common updates to the lab website.

First, install RVM (ruby version manager).  This will be good to have if you have to work on any ruby or rails projects.

https://rvm.io/rvm/install

After cloning down the repository, run:

  1. ```rvm gemset create lab-website```
  2. ```rvm gemset use lab-website```
  3. ```gem install jekyll```
  4. ```jekyll serve``` and test locally on port 4000

#### Add new member data & upload photo

  1. From root directory, _data/members.yml
  2. From root directory, _site/assets/img

#### Update Alumni, Collaborators or Gari's bio
  1. From root directory, __people/__
    * you'll notice your changes reflected in the respective _site/ files

#### Update Info, Ethics & Jobs Page
  1. From root directory, __info.md__, __ethics.md__ and __jobs.md__

Please resist the urge to delete what may appear to be redundant files. They are not.  You may consider restructuring if you have nothing better to do, but do so at your own risk. Have a nice day.
