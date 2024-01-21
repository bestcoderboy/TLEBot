import mwparserfromhell


def extract_infobox(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    infobox = None

    # Find the first template (assumed to be the infobox)
    for template in wikicode.filter_templates():
        infobox = template
        break

    return infobox


def infobox_to_dict(infobox):
    if infobox:
        # Convert infobox to a dictionary
        infobox_dict = {param.name.strip_code().strip(): param.value.strip_code().strip() for param in infobox.params}
        return infobox_dict
    else:
        return None


def convert_wikitext_to_dict(wikitext):
    infobox = extract_infobox(wikitext)
    dict_output = infobox_to_dict(infobox)

    if dict_output:
        return dict_output
    else:
        return None
