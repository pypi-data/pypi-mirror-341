# INTCF

INTCF is short for "If Not Then Create File".

# Purpose

INTCF checks if the file path passes exists, and if not, it will create the file.

# Example

import intcf

path = "C:\\Users\\Admin\\Desktop\\Example.txt"

output = intcf.main(path) (optional if you want print)
print(output) (optional if you want print)

intcf.main(path) (Do this if you dont want output)