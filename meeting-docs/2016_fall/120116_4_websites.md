# Thursday, Dec 1 2016, Notes

## Recap of our 5th meeting this semester!
First of all: cookies from Essence Bakery!

Thanks for stopping by to the people who ate cookies today! 
We had a great meeting demonstrating how easy it actually is to make a cool-looking website.

Wanda Feng made a very helpful 
[guide to making a website](https://docs.google.com/document/d/1_loQMuYhhYjqprTG8lOle1nWj5Y6o4mQmV2R_h8bWxY/edit?usp=sharing
) 
and attaching it 
to your reserved ASU server space (available for grad students, 
postdocs and faculty members). Together, we went through the process of 
personalizing an HTML template from http://www.styleshout.com/free-templates/ 
which contains lots of fancy styles to choose from.

Michael Ruppert went into more detail on writing raw HTML code, 
and his example has been uploaded to github 
[here](https://github.com/prickly-pythons/prickly-pythons/tree/master/code_from_meetings/websites/produce_website_example). 

And Karen mentioned these two sites that make it easy to create a webpage without knowledge of HTML, for free: 

http://www.wix.com/

https://www.weebly.com/

Finally, you can have your ASU website (public.asu.edu/~your-ASU-username) 
redirect to your personal website (made with e.g. one of the above), 
by adding one line to the index.html file on the ASU server. 
Basically your index.html file only has to contain this line:
```
<HEAD><meta http-equiv="refresh" content="0; URL='<your-website>'" /></HEAD>
```
where <your-website> is the address for your website. 
To edit the index.html file, you have to make sure that your ASU webpage hosting 
is activated as described in Wandas document, then SSH into the server:
```
ssh your-ASU-username@general.asu.edu
```
and edit the index.html file in the www/ folder.
