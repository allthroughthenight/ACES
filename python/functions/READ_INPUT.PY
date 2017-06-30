
def READ_INPUT(prompt, min, max):
    value = eval(raw_input(prompt))

    if (value < min or value > max):
        print("Value must be betwwen %-6.2f and %-6.2f\n" % (min, max))
        exit(1)

    return value
