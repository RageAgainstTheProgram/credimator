# credimator

This program creates video credits from a simple textfile. 
Simply write your content in the program-secific [syntax](#syntax) and it will generate your credits.

Running `python credimator.py examples/oppenheimerShort.txt examples/example.gif` gets you 
this video:

<img src ="examples/example.gif">

## Syntax
Every line starting with `#` is a comment. Lines that include `#` will be comments from the 
character until the end of line.

### Settings
The file starts with your video settings. Following settings are availabe:

* `width` -> video width *default: 1920*
* `height` -> video height *default: 1080*
* `background color` -> tuple in RGBA *default: (0, 0, 0, 1)*
* `text color` -> tuple in RGB *default: (255, 255, 255)*
* `font` -> path to the font you want to use 
* `fps` -> frame rate in frames per seccond *default: 25*
* `orientation` -> **not included yet**
* `text size` -> text size in px
* `line space` -> line space in px
* `speed` -> video speed depending on fps
* `box separator` -> separator used in block type "box"
* `border` -> border to the left and right video edges in px
* `tuple space` -> space between left and right site in block tuple
* `block offset` -> space between to blocks
* `right font` -> font for the right side of a tuple. THis is also the font 
for every other text exept for the left side of a tuple
* `left font` -> font for the left side of a tuple

>Note: The order of the settings is irrelevant but look after your spelling as this is what
>the program uses to link the settings


### Block definition
Each block has a type. The type can be *tuple*, *table*, or *box*. These types define which
textlayout to choose.

The block definition looks like this:

```
*headline*(headlinetype, blocktype){

    content

}
```
If your blocktype is *tuple* you have to use following definition:

```
*headline*(headlinetype, blocktype){
    
    left content: right content

}
```

You can use as much whitespace as you want as it will be ignored.

If the left content of your tuple is to long to fit in line there will be a newline fot the rest.
The right content of a tuple will be placed at the last line of the left content.

The layout is completely made by the program but you have options to influence it. The main way to do so
is by changeing `block offset`. This defines the space that is to the end of a block. This area has no
content. If you want you blocks to have a bigger offset simply increase the value of `block offset`.
The space between a previous block and a headline is calculated by the program depending on the healdinetype
that you enter. Also the space between the headline and the following block content depends on the 
headlinetype.

>Note: `block offset` is allways added to your block mo matter which headlintype your next block uses.