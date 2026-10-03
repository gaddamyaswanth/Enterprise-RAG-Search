import re


def split_text(text):

    # Clean spaces

    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()


    # Split using section headings

    sections = re.split(
        r'(Employee Handbook|Leave Policy|Information Security Policy)',
        text
    )


    chunks = []


    current = ""


    for part in sections:

        if part.strip():

            current += part


            if len(current) > 150:

                chunks.append(
                    current.strip()
                )

                current = ""


    if current:

        chunks.append(
            current.strip()
        )


    return chunks