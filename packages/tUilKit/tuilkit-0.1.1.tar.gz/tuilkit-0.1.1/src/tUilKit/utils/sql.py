# src/utilsbase/utils/sql.py

# Initialize Negation
def add_filter(negate, condition):
    if negate:
        return f" AND NOT ({condition})"
    return f" AND ({condition})"

