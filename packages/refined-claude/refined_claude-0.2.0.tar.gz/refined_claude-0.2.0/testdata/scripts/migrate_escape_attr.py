#!/usr/bin/env python3
import re
import sys

# Define a regex pattern to match XML attributes.
# This pattern matches an attribute name (possibly with a colon for namespaced attributes),
# then an equal sign with optional spaces, then a quoted value (using either double or single quotes).
# The DOTALL flag ensures that newlines inside the attribute value are captured.
attribute_pattern = re.compile(
    r'(\w+(?::\w+)*\s*=\s*)(["\'])(.*?)\2',
    re.DOTALL
)

def escape_attr_value(value: str) -> str:
    """
    Escape the attribute value by replacing backslashes and newline characters
    (plus other common whitespace, if desired) with their escaped forms.
    Order is important: first escape backslashes to avoid double conversion.
    """
    # Escape backslashes.
    value = value.replace('\\', '\\\\')
    # Escape newline, carriage return, and tab characters.
    value = value.replace('\n', '\\n')
    value = value.replace('\r', '\\r')
    value = value.replace('\t', '\\t')
    return value

def attribute_replacer(match: re.Match) -> str:
    """
    Given a regex match corresponding to an attribute,
    return a new string with the attribute value modified.
    """
    # Group breakdown:
    # group(1): attribute name and the '=' including any spaces.
    # group(2): the quote character used (single or double).
    # group(3): the attribute value to process.
    prefix = match.group(1)
    quote = match.group(2)
    original_value = match.group(3)
    
    # Process the attribute value with our escape rules.
    escaped_value = escape_attr_value(original_value)
    
    # Rebuild the attribute assignment.
    return f"{prefix}{quote}{escaped_value}{quote}"

def convert_xml_file(input_filename: str, output_filename: str = None) -> None:
    """
    Read an XML file, process every attribute so that all backslashes
    and newlines (and optionally other whitespace) are escaped,
    and then output the transformed XML.
    If output_filename is provided, the result is written to that file.
    Otherwise, it is printed on stdout.
    """
    with open(input_filename, "r", encoding="utf-8") as file:
        xml_data = file.read()
    
    # Replace all attribute occurrences using our replacer function.
    converted_xml = attribute_pattern.sub(attribute_replacer, xml_data)
    
    if output_filename:
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(converted_xml)
        print(f"Conversion complete. Output written to {output_filename}")
    else:
        print(converted_xml)

def main():
    """
    Command-line interface for the converter.
    Usage:
        python converter.py input.xml [output.xml]
    If output.xml is omitted, the result is printed to stdout.
    """
    if len(sys.argv) < 2:
        print("Usage: python converter.py input.xml [output.xml]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None
    convert_xml_file(input_file, output_file)

if __name__ == "__main__":
    main()
