# TagTex
Creating custom nametags, badges. Planning to use Python + LaTeX only.

### Preparation:
- you need python
- install dependencies (i would recomend using a virtual enviornment (but up to you to figure out how and if))
```shell
pip install -r requirements.txt
```
- you need latex (texlive for example)
- additional not included in must texlive instalations
- [texlive-lang](https://wiki.archlinux.org/title/TeX_Live/CJK)

### Example usage:
```shell
python main.py -c <comp id>
```
Output is stored in tex/content.tex and contains all relevant info for competitor tags. Additional tex/name.tex will be created, only containing comp name.
If you want to sort the nametags alphabetically, just add `-o name` to the script. (The default is `-o id` which sorts by time of registration, i.e. the WCA Live ID.)

In order to get a pdf do
```shell
cd tex
pdflatex lables-tamplate.tex
```
It is advisable to check with a 100% scaled view of the resulting PDF if the size fits with your physical nametags before printing and cutting. The labels package documentation can assist with choosing other dimensions for whitespace on the sheets or a different setup of the grid, and the current example has been tested with 55 x 90 mm tags.

#### Used at
- Rheinland-Pfalz Open 2023
- Everstädter Einsteiger Event / Darmstadt Dodecahedron Days 2023
- Kölner Kubing 2023


# todo

- fix hack with ä
- fix hack with ó
- gibt bestimmt noch weitere charackter, die zu fehlern führen, müsste man dann auch fixen
- duplex drucker
    - welp latex kann das wohl nicht so einfach
    - python schon
    - plan ein fuer windows absolut nicht benutzbares skrip produzieren, was dann auch die order fuer duplex printers fixt
        - in even und odd pages splitten
        - die dann wieder zusammenordnen 
        - es ist zu spaet fuer sinnvolle ideen
- man kann noch über flaggen bei ländern nachdenken
