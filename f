[33mcommit 5803e03e450d426f271829f0e4b034c2d1cd25ae[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mdevelop[m[33m)[m
Author: Daksh <164284890+DakshKr@users.noreply.github.com>
Date:   Mon Feb 17 11:03:34 2025 +0000

    Basic Structure of the Assembler

[1mdiff --git a/Assembler.py b/Assembler.py[m
[1mindex bb62d81..be75437 100644[m
[1m--- a/Assembler.py[m
[1m+++ b/Assembler.py[m
[36m@@ -97,7 +97,7 @@[m [mdef convert_to_binary( code, labels ):[m
 [m
         if instruction not in opcodes_dict:[m
             sys.exit(f"Error: Unknown instruction '{instruction}' at line {line_number}" )[m
[31m-        [m
[32m+[m
         match instruction_data["type"]:[m
 [m
             case "R":[m
[36m@@ -127,4 +127,4 @@[m [mdef convert_to_binary( code, labels ):[m
 [m
 [m
 if __name__ == "__main__":[m
[31m-    main()[m
[32m+[m[32m    main()[m
\ No newline at end of file[m
