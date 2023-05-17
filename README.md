# Fň Script
## Syntax
```
input_file.jpg -> output_file.jpg;
    func0;
    func1: p0, p1; comment
    func2: p0, p1, p2;
```
## Comments
Everything after a `;` is a comment and is ignored.
## Functions
| Function | Param Count | Param 0 | Param 1 | Param 2   |
|----------|-------------|---------|---------|-----------|
| vrt      | 0           |         |         |           |
| hor      | 0           |         |         |           |
| spl      | 2           | Filter  | Groups  |           |
| srt      | 3(2)        | Filter  | Divider | Remainder |

| Param     | Description                             | Type |
|-----------|-----------------------------------------|------|
| Filter    | name of filter to use                   | str  |
| Groups    | number of groups to split into          | int  |
| Divider   | for n-th streak in line n % Divider = R | int  |
| Remainder | sort the streak if R = Remainder        | int  |
#### Special param: a
Use `a` to sort all streaks.
Replaces the params 1 and 0 in the srt function.    
`srt: red, a;` = `srt: red, 1, 0;`
### vrt
Reads image file as columns.
### hor
Reads image file as rows.
### spl
Splits lines into streaks.    
`spl: brg, 2;` Splits lines into streaks of lighter and darker pixels.
### srt
Sorts streaks.    
`srt: brg, a;` Sorts all streaks by brightness.    
`srt: brg, 2, 0;` Sorts every second streak by brightness.    
## Filters
| Filter | Description                    |
|--------|--------------------------------|
| red    | value of red channel           |
| blu    | value of blue channel          |
| grn    | value of green channel         |
| sat    | saturation                     |
| val    | value of the brightest channel |
| brg    | average of all channels        |
| lum    | perceived luminance            |
| rnd    | random value                   |

# Dependencies
python3    
alive-progress    
numpy    
