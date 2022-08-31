# Symbol comparator

This python script has been created to ease symbol comparison between 2 binaries. 
When adjusting some compilation settings via CMake, the goal was find differences 
and understand it.

Symbol comparator just parse `nm` output and find all symbols that cannot be 
found, or symbols that have different types or sizes.

# Running the example

Clone the project

```
git clone https://github.com/adri1mart1/symbol-comparator.git
cd symbol-comparator
```

Build the example:

```
cd example
mkdir build
cd build
cmake ..
ninja
cd ../..
```

Start the symbol comparison script:

```
python3 symbol-comparator.py --file example\symbol-comparator-example.json
comparing out files
generate nm files using: nm.exe -l -S --size-sort example/build/pgmA.exe > out\example\nm-file_A.txt
generate nm files using: nm.exe -l -S --size-sort example/build/pgmB.exe > out\example\nm-file_B.txt
 ***** file_A file *****
 * location: example/build/pgmA.exe
 * size: 122604
 * nm file number of line: 575
 * missing symbols num: 3
 ******************
 ***** file_B file *****
 * location: example/build/pgmB.exe
 * size: 122586
 * nm file number of line: 574
 * missing symbols num: 2
 ******************
```

The interesting output is under the `out` directory by default. 
You will find 4 files:

 - the `nm` command output for file A.
 - the `nm` command output for file B.
 - the missing symbols in file A.
 - the missing symbols in file B.

## Output example

As an example, the `missing-in-fileA.txt` contains the following line:

```
Symbol s:000000000000001e t:T n:_Z3barv
```

Which is the symbol for the function (attribute `T`):

```
void bar() {
	std::puts("bar");
#ifdef REQUIREMENT
	std::puts("another");
#endif
}
```

In mainA.cpp, the `REQUIREMENT` is defined so the function is a bit bigger 
than in mainB.cpp.

The symbol in nm-fileB.txt is:

```
000000014000154e 000000000000002d T _Z3barv
```

Note the size difference `2d` vs `1e`.


Another example is in `missing-in-fileB.txt`

```
Symbol s:0000000000000010 t:d n:_ZL3qux
```

This stands for the static variable (attribute `d`) which is missing in 
mainB.cpp.

# How to use

Copy and update the `config-template.json` file to your needs. 
Start the script.

You have change the default output directory which is hardcoded at the moment.
You may also change the `nm` command to a cross compiled compatible version,
so just replace the `nm` to `arm-none-eabi-nm` in the Python script.

# Known limitations

 - Unit tests are inexistant
 - Dupplicated symbols are not well handled
