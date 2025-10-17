#### UTILS

### Utility function to change sign based on matching string input
def change_sign(pos_or_neg):
    if pos_or_neg in {'RIGHT','FORWARD','UP'}:
        return 1
    else:
        return -1

### UTILS END