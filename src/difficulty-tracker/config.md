#Configuration

### show_tooltip (Default: true)
Display tooltip on difficult change

### tag_name (Default: "dif_")
Name for tag that is used (Warning: should not end with a number!)

### max_difficulty (Default: 10)
Maximum difficulty that can be reached

### only_leech (Default: true)
Only change difficulty when leech tag exist on card

### only_leech_tag_name (Default: leech)
The name of the tag that is used for "only_leech" option

### increase_only_on_review (Default: true)
Only change difficulty when card is review type (not new, learning).
Prevent that the card increase difficulty every time we press again.

### good_reset_all (Default: false)
If card is a review card and used button is not again we reduce the difficulty tag by 1.
When the option changed to true, the difficulty tag gets deleted no matter what difficulty level.

### again_is_good (Default: false)
If Cards has "leech" tag (only_leech_tag_name) set and option changed to true,
Card answer will be change to good, doesn't matter we press again or good.
(With this option we can increase the difficulty of our card but rates our card with good)