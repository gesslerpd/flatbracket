# flatbracket

Small shareable encoding for single-elimination tournament brackets (e.g. March Madness)

## Usage

Program relies on newline delimited "teams" file listing all tournament teams in order
of initial tournament matchups. Examples of "teams" file can be found in the `brackets/` folder.

### Create

    python -m flatbracket brackets/2022/womens
    South Carolina vs. Howard
    [0/1]: 0
    ...
    ...
    ...
    South Carolina vs. Connecticut
    [0/1]: 0

    Bracket: QFYEEmTKoig

### View

    $ python -m flatbracket brackets/2022/mens FoASVv4ou3U

```mermaid
flowchart LR
    64-0[Gonzaga vs. Georgia St.] --> 32-0
    64-1[Boise St. vs. Memphis] --> 32-0
    64-2[Connecticut vs. N. Mex St.] --> 32-1
    64-3[Arkansas vs. Vermont] --> 32-1
    64-4[Alabama vs. RUTG/ND] --> 32-2
    64-5[Texas Tech vs. Montana St.] --> 32-2
    64-6[MICHST vs. Davidson] --> 32-3
    64-7[Duke vs. CSFULL] --> 32-3
    64-8[Baylor vs. Norfolk St.] --> 32-4
    64-9[N. Carolina vs. Marquette] --> 32-4
    64-10[MARYCA vs. WYO/IND] --> 32-5
    64-11[UCLA vs. Akron] --> 32-5
    64-12[Texas vs. Va. Tech] --> 32-6
    64-13[Purdue vs. Yale] --> 32-6
    64-14[Murray St. vs. San Fran.] --> 32-7
    64-15[Kentucky vs. St. Peter's] --> 32-7
    64-16[Arizona vs. WRST/BRY] --> 32-8
    64-17[Seton Hall vs. TCU] --> 32-8
    64-18[Houston vs. UAB] --> 32-9
    64-19[Illinois vs. Chattanooga] --> 32-9
    64-20[Colo. St. vs. Michigan] --> 32-10
    64-21[Tennessee vs. Longwood] --> 32-10
    64-22[Ohio St. vs. Loyola Chicago] --> 32-11
    64-23[Villanova vs. Delaware] --> 32-11
    64-24[Kansas vs. TXSO/TXCC] --> 32-12
    64-25[SDGST vs. Creighton] --> 32-12
    64-26[Iowa vs. Richmond] --> 32-13
    64-27[Providence vs. S. Dakota St.] --> 32-13
    64-28[LSU vs. Iowa St.] --> 32-14
    64-29[Wisconsin vs. Colgate] --> 32-14
    64-30[USC vs. Miami] --> 32-15
    64-31[Auburn vs. Jax. State] --> 32-15
    32-0[Gonzaga vs. Memphis] --> 16-0
    32-1[N. Mex St. vs. Arkansas] --> 16-0
    32-2[RUTG/ND vs. Texas Tech] --> 16-1
    32-3[MICHST vs. Duke] --> 16-1
    32-4[Baylor vs. N. Carolina] --> 16-2
    32-5[MARYCA vs. UCLA] --> 16-2
    32-6[Texas vs. Purdue] --> 16-3
    32-7[Murray St. vs. St. Peter's] --> 16-3
    32-8[Arizona vs. TCU] --> 16-4
    32-9[Houston vs. Illinois] --> 16-4
    32-10[Michigan vs. Tennessee] --> 16-5
    32-11[Ohio St. vs. Villanova] --> 16-5
    32-12[Kansas vs. Creighton] --> 16-6
    32-13[Richmond vs. Providence] --> 16-6
    32-14[Iowa St. vs. Wisconsin] --> 16-7
    32-15[Miami vs. Auburn] --> 16-7
    16-0[Gonzaga vs. Arkansas] --> 8-0
    16-1[Texas Tech vs. Duke] --> 8-0
    16-2[N. Carolina vs. UCLA] --> 8-1
    16-3[Purdue vs. St. Peter's] --> 8-1
    16-4[Arizona vs. Houston] --> 8-2
    16-5[Michigan vs. Villanova] --> 8-2
    16-6[Kansas vs. Providence] --> 8-3
    16-7[Iowa St. vs. Miami] --> 8-3
    8-0[Arkansas vs. Duke] --> 4-0
    8-1[N. Carolina vs. St. Peter's] --> 4-0
    8-2[Houston vs. Villanova] --> 4-1
    8-3[Kansas vs. Miami] --> 4-1
    4-0[Duke vs. N. Carolina] --> 2-0
    4-1[Villanova vs. Kansas] --> 2-0
    2-0[N. Carolina vs. Kansas] --> 1-0
    1-0[Kansas]
```

    $ python -m flatbracket brackets/2022/mens RANDOM
    Bracket: RANDOM
    UjdRGjmNETg

```mermaid
flowchart LR
    64-0[Gonzaga vs. Georgia St.] --> 32-0
    64-1[Boise St. vs. Memphis] --> 32-0
    64-2[Connecticut vs. N. Mex St.] --> 32-1
    64-3[Arkansas vs. Vermont] --> 32-1
    64-4[Alabama vs. RUTG/ND] --> 32-2
    64-5[Texas Tech vs. Montana St.] --> 32-2
    64-6[MICHST vs. Davidson] --> 32-3
    64-7[Duke vs. CSFULL] --> 32-3
    64-8[Baylor vs. Norfolk St.] --> 32-4
    64-9[N. Carolina vs. Marquette] --> 32-4
    64-10[MARYCA vs. WYO/IND] --> 32-5
    64-11[UCLA vs. Akron] --> 32-5
    64-12[Texas vs. Va. Tech] --> 32-6
    64-13[Purdue vs. Yale] --> 32-6
    64-14[Murray St. vs. San Fran.] --> 32-7
    64-15[Kentucky vs. St. Peter's] --> 32-7
    64-16[Arizona vs. WRST/BRY] --> 32-8
    64-17[Seton Hall vs. TCU] --> 32-8
    64-18[Houston vs. UAB] --> 32-9
    64-19[Illinois vs. Chattanooga] --> 32-9
    64-20[Colo. St. vs. Michigan] --> 32-10
    64-21[Tennessee vs. Longwood] --> 32-10
    64-22[Ohio St. vs. Loyola Chicago] --> 32-11
    64-23[Villanova vs. Delaware] --> 32-11
    64-24[Kansas vs. TXSO/TXCC] --> 32-12
    64-25[SDGST vs. Creighton] --> 32-12
    64-26[Iowa vs. Richmond] --> 32-13
    64-27[Providence vs. S. Dakota St.] --> 32-13
    64-28[LSU vs. Iowa St.] --> 32-14
    64-29[Wisconsin vs. Colgate] --> 32-14
    64-30[USC vs. Miami] --> 32-15
    64-31[Auburn vs. Jax. State] --> 32-15
    32-0[Gonzaga vs. Memphis] --> 16-0
    32-1[Connecticut vs. Arkansas] --> 16-0
    32-2[RUTG/ND vs. Texas Tech] --> 16-1
    32-3[Davidson vs. Duke] --> 16-1
    32-4[Norfolk St. vs. Marquette] --> 16-2
    32-5[WYO/IND vs. UCLA] --> 16-2
    32-6[Va. Tech vs. Yale] --> 16-3
    32-7[Murray St. vs. Kentucky] --> 16-3
    32-8[WRST/BRY vs. Seton Hall] --> 16-4
    32-9[Houston vs. Illinois] --> 16-4
    32-10[Michigan vs. Tennessee] --> 16-5
    32-11[Loyola Chicago vs. Villanova] --> 16-5
    32-12[Kansas vs. Creighton] --> 16-6
    32-13[Iowa vs. S. Dakota St.] --> 16-6
    32-14[Iowa St. vs. Wisconsin] --> 16-7
    32-15[USC vs. Auburn] --> 16-7
    16-0[Memphis vs. Connecticut] --> 8-0
    16-1[RUTG/ND vs. Duke] --> 8-0
    16-2[Marquette vs. UCLA] --> 8-1
    16-3[Va. Tech vs. Murray St.] --> 8-1
    16-4[Seton Hall vs. Houston] --> 8-2
    16-5[Tennessee vs. Villanova] --> 8-2
    16-6[Kansas vs. Iowa] --> 8-3
    16-7[Iowa St. vs. Auburn] --> 8-3
    8-0[Connecticut vs. RUTG/ND] --> 4-0
    8-1[Marquette vs. Va. Tech] --> 4-0
    8-2[Houston vs. Tennessee] --> 4-1
    8-3[Kansas vs. Iowa St.] --> 4-1
    4-0[Connecticut vs. Marquette] --> 2-0
    4-1[Houston vs. Iowa St.] --> 2-0
    2-0[Marquette vs. Iowa St.] --> 1-0
    1-0[Marquette]
```

## Encoding

Brackets are encoded in URL-safe base64 for easy shareability.
The decoded bytes are a bit sequence storing the results of each matchup in order of tournament rounds,
starting with the first round and ending with the championship.

For instance, a bracket for the 2022 March Madness: Men's tournament can be encoded into 11 characters (`FoASVv4ou3U`).

```python
# FoASVv4ou3U
BRACKET_2022 = 0b1_1_1_0_1_0_1_10_11_10_11_0010_1000_1111_1110_01010110_00010010_10000000_00010110.to_bytes(8, "little")
```

## Output

Program outputs in the [Mermaid](https://mermaid.js.org/) diagramming format.
It's possible to run the program with partial bracket information,
but diagram will not be a single connected component.

- [Interactive viewer/editor](https://mermaid.live/)
- [Embedded in GitHub Flavored Markdown](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/)
````
```mermaid
flowchart LR
    64-0[Gonzaga vs. Georgia St.] --> 32-0   
    64-1[Boise St. vs. Memphis] --> 32-0     
    64-2[Connecticut vs. N. Mex St.] --> 32-1
    64-3[Arkansas vs. Vermont] --> 32-1      
    64-4[Alabama vs. RUTG/ND] --> 32-2       
    64-5[Texas Tech vs. Montana St.] --> 32-2
    64-6[MICHST vs. Davidson] --> 32-3       
    64-7[Duke vs. CSFULL] --> 32-3
    64-8[Baylor vs. Norfolk St.] --> 32-4    
    64-9[N. Carolina vs. Marquette] --> 32-4 
    64-10[MARYCA vs. WYO/IND] --> 32-5
    64-11[UCLA vs. Akron] --> 32-5
    64-12[Texas vs. Va. Tech] --> 32-6
    64-13[Purdue vs. Yale] --> 32-6
    64-14[Murray St. vs. San Fran.] --> 32-7
    64-15[Kentucky vs. St. Peter's] --> 32-7
    64-16[Arizona vs. WRST/BRY] --> 32-8
    64-17[Seton Hall vs. TCU] --> 32-8
    64-18[Houston vs. UAB] --> 32-9
    64-19[Illinois vs. Chattanooga] --> 32-9
    64-20[Colo. St. vs. Michigan] --> 32-10
    64-21[Tennessee vs. Longwood] --> 32-10
    64-22[Ohio St. vs. Loyola Chicago] --> 32-11
    64-23[Villanova vs. Delaware] --> 32-11
    64-24[Kansas vs. TXSO/TXCC] --> 32-12
    64-25[SDGST vs. Creighton] --> 32-12
    64-26[Iowa vs. Richmond] --> 32-13
    64-27[Providence vs. S. Dakota St.] --> 32-13
    64-28[LSU vs. Iowa St.] --> 32-14
    64-29[Wisconsin vs. Colgate] --> 32-14
    64-30[USC vs. Miami] --> 32-15
    64-31[Auburn vs. Jax. State] --> 32-15
    32-0[Gonzaga vs. Memphis] --> 16-0
    32-1[N. Mex St. vs. Arkansas] --> 16-0
    32-2[RUTG/ND vs. Texas Tech] --> 16-1
    32-3[MICHST vs. Duke] --> 16-1
    32-4[Baylor vs. N. Carolina] --> 16-2
    32-5[MARYCA vs. UCLA] --> 16-2
    32-6[Texas vs. Purdue] --> 16-3
    32-7[Murray St. vs. St. Peter's] --> 16-3
    32-8[Arizona vs. TCU] --> 16-4
    32-9[Houston vs. Illinois] --> 16-4
    32-10[Michigan vs. Tennessee] --> 16-5
    32-11[Ohio St. vs. Villanova] --> 16-5
    32-12[Kansas vs. Creighton] --> 16-6
    32-13[Richmond vs. Providence] --> 16-6
    32-14[Iowa St. vs. Wisconsin] --> 16-7
    32-15[Miami vs. Auburn] --> 16-7
    16-0[Gonzaga vs. Arkansas] --> 8-0
    16-1[Texas Tech vs. Duke] --> 8-0
    16-2[N. Carolina vs. UCLA] --> 8-1
    16-3[Purdue vs. St. Peter's] --> 8-1
    16-4[Arizona vs. Houston] --> 8-2
    16-5[Michigan vs. Villanova] --> 8-2
    16-6[Kansas vs. Providence] --> 8-3
    16-7[Iowa St. vs. Miami] --> 8-3
    8-0[Arkansas vs. Duke] --> 4-0
    8-1[N. Carolina vs. St. Peter's] --> 4-0
    8-2[Houston vs. Villanova] --> 4-1
    8-3[Kansas vs. Miami] --> 4-1
    4-0[Duke vs. N. Carolina] --> 2-0
    4-1[Villanova vs. Kansas] --> 2-0
    2-0[N. Carolina vs. Kansas] --> 1-0
    1-0[Kansas]
```
````
