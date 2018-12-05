from bs4 import BeautifulSoup


def get_text_from_bs(bs_obj):
    break_elements = ["p", "br"]
    for break_element in break_elements:
        # We replace all html breaks with text new lines
        breaks = bs_obj.find_all(break_element)
        for break_obj in breaks:
            break_obj.replace_with("\n{}".format(break_obj.get_text()))

    return bs_obj.get_text().strip()
