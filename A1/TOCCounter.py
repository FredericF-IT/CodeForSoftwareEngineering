loctot = 0
locne = 0
locpars = 0

with open("MyQuickSort.java") as code_file:
    line = code_file.readline()
    is_multi_comment = False

    while line:
        loctot += 1 # there is another line

        line = line.strip() # removes all whitespaces
        if not line:
            line = code_file.readline() # get next line
            continue
        locne += 1 # line has non-whitespace characters
        
        # Cases:
        # chars /* chars */ chars <- has non commment content at start / end
        # chars // /* <- does not start multi line comment
        # /* // */ <- is fine, still commented out either way
        
        is_just_comment = line.startswith("//")
        single_priority = -1
        if is_just_comment:
            single_priority = line.index("//")  # Comments block other types of comments, 
                                                # the line "continue; // comment /* ..." does not start a multi-line comment
                                                # so we measure which comes first if both appear

        multi_priority = -1
        hasCharsBefore = False                  # If this is True, we increase locpars
        if "/*" in line:
            multi_priority = line.index("/*")
            if not is_just_comment:
                is_multi_comment = True         # multi-line comment is only comment type in line
                hasCharsBefore = multi_priority > 0
            elif multi_priority < single_priority:
                is_multi_comment = True         # multi-line comment begins before single line comment (/* ... // ... */)
                is_just_comment = False         # It is not a // comment, meaning that */ should not be ignored
                hasCharsBefore = multi_priority > 0
            else:                               # single line occurs before multi-line comment
                hasCharsBefore = single_priority > 0

        hasCharsAfter = False                   # If this is True, we increase locpars
        is_multi_comment_end = False
        if "*/" in line:
            if not is_just_comment:
                is_multi_comment = False        # Multi-line comment ends here
                is_multi_comment_end = True
                hasCharsAfter = not line.endswith("*/")
                                                # There are characters after end of mult-line comment

        if not is_just_comment and (not is_multi_comment or hasCharsBefore) and (not is_multi_comment_end or hasCharsAfter):
            locpars += 1

        line = code_file.readline()             # get next line

print("LOCtot  |", str(loctot).rjust(10))
print("LOCne   |", str(locne).rjust(10))
print("LOCpars |", str(locpars).rjust(10))
