import random
import sys
import time
import subprocess
import os

# Configuration
BATCH_FILE_PATH = "Assets\\Code.bat"  # Default path for batch file output


def finish_program():
    print("\n=== Program finished ===")
    print("Final code:\n")
    print("; ".join(Code))
    print("\n\nExecuting final program...\n")
    execute_code()


def RUN(code_line, answer_var="", loop_stack_ref=None):
    """Run a single line of Double Line code and return updated answer"""
    line = code_line.strip()
    answer = answer_var

    # say - Output text
    if line.startswith("say "):
        text = line[4:].replace("*answer*", answer)
        print(text)

    # ask - User input
    elif line.startswith("ask "):
        answer = input(line[4:] + " ")

    # var - Set variable
    elif line.startswith("var *"):
        parts = line.split("=", 1)
        var_num = int(parts[0].split("*")[1])
        if len(parts) > 1:
            value = parts[1].strip()
            if value == "*answer*":
                vars[var_num] = answer
            else:
                vars[var_num] = value

    # sayVar - Output variable
    elif line.startswith("sayVar *"):
        var_num = int(line.split("*")[1])
        print(vars[var_num])

    # varName - Set variable name
    elif line.startswith("varName *"):
        parts = line.split("=", 1)
        var_num = int(parts[0].split("*")[1])
        if len(parts) > 1:
            name = parts[1].strip()
            varNames[var_num] = name

    # sayVarName - Output variable name
    elif line.startswith("sayVarName *"):
        var_num = int(line.split("*")[1])
        print(varNames[var_num])

    # varMath - Mathematical operations and comparisons
    elif line.startswith("varMath *"):
        parts = line.split("=", 1)
        var_num = int(parts[0].split("*")[1])
        if len(parts) > 1:
            expression = parts[1].strip()
            # Replace variables with their values
            for i in range(100):
                expression = expression.replace(f"*{i}", str(vars[i]))
            expression = expression.replace("*answer*", answer)

            try:
                has_comparison = any(op in expression for op in ["==", "!=", ">=", "<=", ">", "<"])
                if has_comparison:
                    result = eval(expression)
                    vars[var_num] = "1" if result else "0"
                else:
                    result = eval(expression)
                    vars[var_num] = str(result)
            except:
                print(f"Error in varMath: {line}")

    # random - Random number
    elif line.startswith("random *"):
        var_num = int(line.split("*")[1].split("#")[0])
        parts = line.split("#")
        if len(parts) >= 3:
            min_val = int(parts[1])
            max_val = int(parts[2])
            vars[var_num] = str(random.randint(min_val, max_val))

    return answer


def execute_code():
    """Execute the complete code with enhanced loop support"""
    answer = ""
    j = 0
    loop_stack = []  # Stack for nested loops: [(start_index, loop_counter, max_iterations)]

    while j < len(Code):
        line = Code[j].strip()

        # if - Condition (needs special handling)
        if line.startswith("if "):
            # Format: if *1 == *2 # say Hello
            line_parts = line.split("#", 1)
            condition_part = line_parts[0].strip()

            if len(line_parts) > 1:
                action_part = line_parts[1].strip()

                # Parse condition
                condition_tokens = condition_part.split()
                if len(condition_tokens) >= 4:
                    def resolve_value(token):
                        if token == "*answer*":
                            return answer
                        elif token.startswith("*"):
                            return vars[int(token.replace("*", ""))]
                        return token

                    val1 = resolve_value(condition_tokens[1])
                    operator = condition_tokens[2]
                    val2 = resolve_value(condition_tokens[3])

                    condition_met = False
                    if operator == "==":
                        condition_met = (val1 == val2)
                    elif operator == "!=":
                        condition_met = (val1 != val2)
                    elif operator == ">":
                        try:
                            condition_met = (float(val1) > float(val2))
                        except:
                            condition_met = False
                    elif operator == "<":
                        try:
                            condition_met = (float(val1) < float(val2))
                        except:
                            condition_met = False
                    elif operator == ">=":
                        try:
                            condition_met = (float(val1) >= float(val2))
                        except:
                            condition_met = False
                    elif operator == "<=":
                        try:
                            condition_met = (float(val1) <= float(val2))
                        except:
                            condition_met = False

                    if condition_met:
                        # Special handling for loop control commands
                        if action_part == "endLoop":
                            if loop_stack:
                                loop_stack.pop()
                        elif action_part == "breakLoop":
                            # Find matching endLoop and jump past it
                            if loop_stack:
                                loop_depth = 1
                                k = j + 1
                                while k < len(Code) and loop_depth > 0:
                                    if Code[k].strip() == "loop":
                                        loop_depth += 1
                                    elif Code[k].strip() == "endLoop":
                                        loop_depth -= 1
                                    k += 1
                                j = k - 1
                                loop_stack.pop()
                        else:
                            answer = RUN(action_part, answer, loop_stack)

        # loop - Start loop (simple infinite loop)
        elif line == "loop":
            loop_stack.append([j, 0])  # [start_index, counter] - only 2 elements for infinite loop

        # loopFor - Loop with fixed iterations: loopFor #10
        elif line.startswith("loopFor #"):
            try:
                iterations = int(line.split("#")[1].strip())
                loop_stack.append([j, 0, iterations])  # [start_index, counter, max_iterations]
            except:
                print(f"Error: Invalid loopFor format. Use 'loopFor #number'")

        # loopWhile - Loop with condition: loopWhile *1 < *2
        elif line.startswith("loopWhile "):
            condition_str = line[10:].strip()
            loop_stack.append([j, 0, -1, condition_str])  # Add condition as 4th element

        # repeatLoop - Repeat loop (goes back to loop start)
        elif line == "repeatLoop" or line == "reapitLoop":
            if loop_stack:
                loop_info = loop_stack[-1]
                start_index = loop_info[0]

                # Check if it's a loopFor (has max_iterations as 3rd element, no 4th element)
                if len(loop_info) == 3 and loop_info[2] > 0:
                    loop_info[1] += 1  # Increment counter
                    if loop_info[1] < loop_info[2]:
                        j = start_index  # Continue looping
                    else:
                        # Loop finished, remove from stack and continue to next line
                        loop_stack.pop()

                # Check if it's a loopWhile (has condition as 4th element)
                elif len(loop_info) == 4:
                    loop_info[1] += 1  # Increment counter
                    condition_str = loop_info[3]
                    # Evaluate condition
                    tokens = condition_str.split()
                    if len(tokens) >= 3:
                        def resolve_value(token):
                            if token == "*answer*":
                                return answer
                            elif token.startswith("*"):
                                return vars[int(token.replace("*", ""))]
                            return token

                        val1 = resolve_value(tokens[0])
                        operator = tokens[1]
                        val2 = resolve_value(tokens[2])

                        condition_met = False
                        try:
                            if operator == "==":
                                condition_met = (val1 == val2)
                            elif operator == "!=":
                                condition_met = (val1 != val2)
                            elif operator == ">":
                                condition_met = (float(val1) > float(val2))
                            elif operator == "<":
                                condition_met = (float(val1) < float(val2))
                            elif operator == ">=":
                                condition_met = (float(val1) >= float(val2))
                            elif operator == "<=":
                                condition_met = (float(val1) <= float(val2))
                        except:
                            condition_met = False

                        if condition_met:
                            j = start_index
                        else:
                            loop_stack.pop()
                    else:
                        loop_stack.pop()
                else:
                    # Infinite loop (only 2 elements in loop_info)
                    j = start_index
            else:
                print("Error: repeatLoop without loop")

        # endLoop - End loop block
        elif line == "endLoop":
            if loop_stack:
                loop_stack.pop()

        # breakLoop - Exit current loop immediately
        elif line == "breakLoop":
            if loop_stack:
                # Find matching endLoop and jump past it
                loop_depth = 1
                k = j + 1
                while k < len(Code) and loop_depth > 0:
                    if Code[k].strip() in ["loop", "loopFor", "loopWhile"]:
                        loop_depth += 1
                    elif Code[k].strip() == "endLoop":
                        loop_depth -= 1
                    k += 1
                j = k - 1
                loop_stack.pop()

        # continueLoop - Skip to next iteration
        elif line == "continueLoop":
            if loop_stack:
                loop_info = loop_stack[-1]
                start_index = loop_info[0]

                # Check if it's a loopFor (3 elements, no 4th)
                if len(loop_info) == 3 and loop_info[2] > 0:
                    loop_info[1] += 1
                    if loop_info[1] < loop_info[2]:
                        j = start_index
                    else:
                        loop_stack.pop()
                else:
                    # For infinite loops or loopWhile, just jump back
                    j = start_index

        # All other commands - use RUN function
        else:
            answer = RUN(line, answer, loop_stack)

        j += 1

    print("\n=== Execution completed ===\n")


def run_batch_file(path=None):
    """Run the generated batch file"""
    if path is None:
        path = BATCH_FILE_PATH

    if os.path.exists(path):
        subprocess.run([path], shell=True)
        input('\nPress Enter to continue...')
    else:
        print(f"Error: {path} not found!")


def convert_to_batch(code_line):
    """Convert Double Line code to batch file commands"""
    code_line = code_line.strip()

    # say - Output text
    if code_line.startswith('say '):
        text = code_line[4:].replace('*answer', '!answer!')
        # Replace variable references in text - reverse order for multi-digit
        for i in range(99, -1, -1):
            text = text.replace(f'*{i}', f'!var{i}!')
        return f"echo {text}\n"

    # Handle empty say commands (just "say")
    elif code_line == 'say':
        return "echo.\n"

    # ask - User input
    elif code_line.startswith('ask '):
        prompt = code_line[4:]
        return f"set /p answer=\"{prompt}: \"\n"

    # var - Set variable
    elif code_line.startswith('var *'):
        parts = code_line.split("=", 1)
        var_num = parts[0].split("*")[1].strip()
        if len(parts) > 1:
            value = parts[1].strip()
            if value == "*answer":
                return f"set var{var_num}=!answer!\n"
            else:
                # Replace variable references - reverse order for multi-digit
                for i in range(99, -1, -1):
                    value = value.replace(f"*{i}", f"!var{i}!")
                return f"set var{var_num}={value}\n"

    # sayVar - Output variable
    elif code_line.startswith('sayVar *'):
        var_num = code_line.split("*")[1].strip()
        return f"echo !var{var_num}!\n"

    # varMath - Mathematical operations
    elif code_line.startswith('varMath *'):
        parts = code_line.split("=", 1)
        var_num = parts[0].split("*")[1].strip()
        if len(parts) > 1:
            expression = parts[1].strip()
            # Replace variables - do this in reverse order
            for i in range(99, -1, -1):
                expression = expression.replace(f"*{i}", f"!var{i}!")
            expression = expression.replace("*answer*", "!answer!")

            # Check for comparisons
            if "==" in expression:
                left, right = expression.split("==", 1)
                return f"if {left.strip()} EQU {right.strip()} (set var{var_num}=1) else (set var{var_num}=0)\n"
            elif "!=" in expression:
                left, right = expression.split("!=", 1)
                return f"if {left.strip()} NEQ {right.strip()} (set var{var_num}=1) else (set var{var_num}=0)\n"
            elif ">=" in expression:
                left, right = expression.split(">=", 1)
                return f"if {left.strip()} GEQ {right.strip()} (set var{var_num}=1) else (set var{var_num}=0)\n"
            elif "<=" in expression:
                left, right = expression.split("<=", 1)
                return f"if {left.strip()} LEQ {right.strip()} (set var{var_num}=1) else (set var{var_num}=0)\n"
            elif ">" in expression:
                left, right = expression.split(">", 1)
                return f"if {left.strip()} GTR {right.strip()} (set var{var_num}=1) else (set var{var_num}=0)\n"
            elif "<" in expression:
                left, right = expression.split("<", 1)
                return f"if {left.strip()} LSS {right.strip()} (set var{var_num}=1) else (set var{var_num}=0)\n"
            else:
                return f"set /a var{var_num}={expression}\n"

    # random - Random number
    elif code_line.startswith('random *'):
        var_num = code_line.split("*")[1].split("#")[0].strip()
        parts = code_line.split("#")
        if len(parts) >= 3:
            min_val = parts[1].strip()
            max_val = parts[2].strip()
            range_val = int(max_val) - int(min_val) + 1
            return f"set /a var{var_num}=!random! %% {range_val} + {min_val}\n"

    # loop - Start loop
    elif code_line == 'loop':
        return ":loop\n"

    # loopFor - For loop with counter
    elif code_line.startswith('loopFor #'):
        iterations = code_line.split("#")[1].strip()
        return f"set loopCounter=0\n:loopFor\n"

    # repeatLoop - Repeat loop
    elif code_line == 'repeatLoop' or code_line == 'reapitLoop':
        return "goto loop\n"

    # breakLoop - Exit loop
    elif code_line == 'breakLoop':
        return "goto :endloop\n"

    # varName and sayVarName
    elif code_line.startswith('varName *') or code_line.startswith('sayVarName *'):
        return f"rem {code_line}\n"

    return None


def export_to_batch(bat_path=None):
    """Export current code to batch file"""
    if bat_path is None:
        bat_path = BATCH_FILE_PATH

    BatLines = [
        "@echo off\n",
        "setlocal enabledelayedexpansion\n",
        "title Double Line Program\n",
        "color 0A\n",
        "\n",
        "rem Initialize variables\n",
        "set answer=\n"
    ]

    # Initialize all variables
    for i in range(100):
        BatLines.append(f"set var{i}=NONE\n")

    BatLines.append("\n")
    BatLines.append("goto :main\n\n")

    # Generate the main code
    BatLines.append(":main\n")

    for line in Code:
        # Special handling for if statements
        if line.strip().startswith('if '):
            line_parts = line.strip().split("#", 1)
            if len(line_parts) > 1:
                condition_part = line_parts[0].strip()
                action_part = line_parts[1].strip()

                # Parse condition
                tokens = condition_part.split()
                if len(tokens) >= 4:
                    var1 = tokens[1].replace("*", "var")
                    operator = tokens[2]
                    var2 = tokens[3].replace("*", "var")

                    # Convert operator
                    bat_op = operator
                    if operator == "==":
                        bat_op = "EQU"
                    elif operator == "!=":
                        bat_op = "NEQ"
                    elif operator == ">":
                        bat_op = "GTR"
                    elif operator == "<":
                        bat_op = "LSS"
                    elif operator == ">=":
                        bat_op = "GEQ"
                    elif operator == "<=":
                        bat_op = "LEQ"

                    # Convert the action
                    converted_action = convert_to_batch(action_part)
                    if converted_action:
                        BatLines.append(f"if !{var1}! {bat_op} !{var2}! ({converted_action.strip()})\n")
                    else:
                        BatLines.append(f"rem if action not converted: {action_part}\n")

        # Handle loopFor specially
        elif line.strip().startswith('loopFor #'):
            iterations = line.strip().split("#")[1].strip()
            BatLines.append(f"set loopCounter=0\n")
            BatLines.append(f"set loopMax={iterations}\n")
            BatLines.append(f":loopFor\n")
            BatLines.append(f"if !loopCounter! GEQ !loopMax! goto :endloop\n")

        elif line.strip() == 'repeatLoop' or line.strip() == 'reapitLoop':
            # Check if we're in a loopFor
            BatLines.append("set /a loopCounter+=1\n")
            BatLines.append("goto loopFor\n")

        else:
            bat_line = convert_to_batch(line)
            if bat_line:
                BatLines.append(bat_line)
            else:
                BatLines.append(f"rem Unsupported: {line}\n")

    BatLines.append("\n:endloop\n")
    BatLines.append("endlocal\n")
    BatLines.append("exit\n")

    with open(bat_path, "w", encoding="utf-8") as file:
        file.writelines(BatLines)

    print(f"\nCode exported to {bat_path}")


print("=" * 50)
print(" Double Line Programming Language - Enhanced")
print("=" * 50)
print("Type 'help' to see all commands")
print("Type 'end' to finish and execute your program")
print(f"Batch file output: {BATCH_FILE_PATH}")
print("=" * 50 + "\n")

Code = []
vars = ["NONE"] * 100
varNames = ["N0NE"] * 100

while True:
    # Show current code
    if Code:
        print("\nCurrent code:")
        for i, line in enumerate(Code, 1):
            print(f"  {i}: {line}")
        print()

    codeLine = input(">> ")

    # end - Finish program and execute
    if codeLine.strip() == "end":
        finish_program()
        time.sleep(400)
        sys.exit()

    # help - Show help
    if codeLine.strip() == "help":
        print("\n=== Available Code Commands ===")
        print("say <text> - Print text (use *answer* for last input)")
        print("ask <prompt> - Ask user for input")
        print("var *n = <value> - Set variable n to value")
        print("sayVar *n - Print variable n")
        print("varName *n = <name> - Set name for variable n")
        print("sayVarName *n - Print variable name")
        print("varMath *n = <expr> - Calculate math or compare (returns 1/0)")
        print("  Math: *1 + *2, *1 - 5, *1 * 3")
        print("  Compare: *1 == *2, *1 != 5, *1 > *2, *1 < 10")
        print("random *n #min #max - Set variable n to random number")
        print("if *n <op> *m # <action> - Execute action if condition is true")
        print()
        print("=== Loop Commands (ENHANCED!) ===")
        print("loop - Start an infinite loop")
        print("loopFor #<n> - Loop exactly n times")
        print("loopWhile *n <op> *m - Loop while condition is true")
        print("  Example: loopWhile *1 < 10")
        print("repeatLoop - Go back to loop start (continue looping)")
        print("endLoop - Mark end of loop block")
        print("breakLoop - Exit current loop immediately")
        print("continueLoop - Skip to next iteration")
        print()
        print("=== Loop Examples ===")
        print("Example 1 - Count to 10:")
        print("  var *1 = 0")
        print("  loopFor #10")
        print("  varMath *1 = *1 + 1")
        print("  sayVar *1")
        print("  repeatLoop")
        print("  endLoop")
        print()
        print("Example 2 - Loop while condition:")
        print("  var *1 = 0")
        print("  loopWhile *1 < 5")
        print("  sayVar *1")
        print("  varMath *1 = *1 + 1")
        print("  repeatLoop")
        print("  endLoop")
        print()
        print("Example 3 - Break on condition:")
        print("  var *1 = 0")
        print("  loop")
        print("  varMath *1 = *1 + 1")
        print("  sayVar *1")
        print("  if *1 == 5 # breakLoop")
        print("  repeatLoop")
        print("  endLoop")
        print()
        print("=== Helper Commands ===")
        print("run - Run current code (for testing)")
        print("clear - Delete all code")
        print("clear #<n> - Delete line n in Code")
        print("add +<code> at #<n> - Add code at line n in Code")
        print("export - Export code to .bat file")
        print("runbat - Run the exported batch file")
        print("end - Finish and execute program")
        print("exit - Exit without executing")
        print("\nYou can write multiple commands in one line using ';'")
        print("Example: var *1 = 0; loopFor #5; sayVar *1; varMath *1 = *1 + 1\n")
        continue

    # execute - Run code without ending
    if codeLine.strip() == "run":
        if Code:
            print("\n" + "=" * 50)
            print(" Executing current code...")
            print("=" * 50 + "\n")
            execute_code()
            print("=" * 50)
            print(" Execution finished - continuing programming...")
            print("=" * 50 + "\n")
        else:
            print("No code to execute yet!\n")
        continue

    # export - Export to batch file
    if codeLine.strip() == "export":
        if Code:
            export_to_batch()
        else:
            print("No code to export!\n")
        continue

    # runbat - Run batch file
    if codeLine.strip() == "runbat":
        run_batch_file()
        continue

    # exit - Exit without executing
    if codeLine.strip() == "exit":
        print("Exiting without execution...")
        sys.exit()

    # clear - Clear code
    if codeLine.strip() == "clear":
        Code = []
        vars = ["0"] * 100
        varNames = ["N0NE"] * 100
        print("Code cleared!\n")
        continue

    # clear #n - Delete single line
    if codeLine.strip().startswith("clear #"):
        try:
            line_num = int(codeLine.strip().split("#")[1])
            if 1 <= line_num <= len(Code):
                deleted_line = Code.pop(line_num - 1)
                print(f"Deleted line {line_num}: {deleted_line}\n")
            else:
                print(f"Error: Line {line_num} doesn't exist!\n")
        except (ValueError, IndexError):
            print("Error: Use 'clear #number' to delete a line\n")
        continue

    # add - Insert code at specific line
    if codeLine.strip().startswith("add"):
        try:
            parts = codeLine.split(" at ")
            if len(parts) == 2:
                code_part = parts[0].strip()
                if "+" in code_part:
                    addedCode = code_part.split("+", 1)[1].strip()
                else:
                    print("Error: Use format 'add +<code> at #<line>'\n")
                    continue

                line_part = parts[1].strip()
                if "#" in line_part:
                    line_num = int(line_part.replace("#", "").strip())
                else:
                    line_num = int(line_part.strip())

                if 0 <= line_num <= len(Code):
                    Code.insert(line_num, addedCode)
                    print(f"Added '{addedCode}' at line {line_num}\n")
                else:
                    print(f"Error: Line {line_num} is out of range!\n")
            else:
                print("Error: Use format 'add +<code> at #<line>'\n")
        except (ValueError, IndexError) as e:
            print(f"Error: Invalid add command format. Use 'add +<code> at #<line>'\n")
        continue

    # Add code line(s)
    for part in codeLine.split(";"):
        if part.strip():
            Code.append(part.strip())