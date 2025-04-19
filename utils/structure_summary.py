def summarize_structure(text):
    sections = {}
    lines = text.split("\n")
    current_header = None
    for line in lines:
        if line.strip() == "":
            continue
        if line.strip().startswith(("บทที่", "บท", "Chapter")):
            current_header = line.strip()
            sections[current_header] = ""
        elif current_header:
            sections[current_header] += line + " "
    return sections