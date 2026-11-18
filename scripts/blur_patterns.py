"""Pattern for generic wording that replaced a customer name, in a wiki that keeps customer names.

Used by check_evidence.py --generalised-names (rule `generalised-name`) and by
any script that scans for the same wording. Scripts run with `python3 -I`,
which drops the script's directory from sys.path, so callers load this file by
path with load_blur().
"""
import re

BLUR = re.compile(
    r"another (client|customer|pharma|company|account|prospect)"
    r"|previous (client|customer)"
    r"|not named (here|in this wiki)"
    r"|unnamed (client|customer)"
    r"|anonymi[sz]ed (client|customer|reference)"
    r"|(?<!\bis )(?<!\bwas )\b(a|an) (large|big|major|global|european|us|french|german|swiss|danish|japanese"
    r"|top-?\d+|mid-?size|leading) (pharma|pharmaceutical|biotech|nutrition|cpg|medtech"
    r"|diagnostics)\w*( company| client| customer| partner)?"
    r"|\b(customer|client) [A-D]\b"
    r"|\[(customer|client)( name)?\]|<customer>"
    r"|other customer'?s? name",
    re.I,
)


def strip_quotes(line):
    """Remove quoted spans of any length, so a quotation never counts as generalisation."""
    return re.sub(r"“[^“”\n]*”|(?<![\w*])\"[^\"\n]*\"(?![\w])", " ", line)
