REVERSED_ORDER_TAGS = ["NN PRP", "NNP PRP VBP", "WP VB", "WRB VB PRP", "WDT NNS", "VB DT"]


def reversed_word_order(tags):
    result = False
    for predefined in REVERSED_ORDER_TAGS:
        result |= predefined in tags
    return result

