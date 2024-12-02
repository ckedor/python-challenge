from datetime import datetime, timedelta

def reconcile_accounts(transactions1, transactions2):
    """
    Find matches between two lists of transactions.

    For each transaction in `transactions1`, this function finds if there is a match in `transactions2` based on:
      - The date being within ±1 day of the transaction in `transactions1`.
      - Exact match for category, value, and service fields.
      - If two or more transactions from `transactions2` match a single transaction in `transactions1` (besides the date),
        the function considers the match with the transaction having the earliest date.

    Parameters
    ----------
    transactions1 : list of list
        A list of transactions, where each transaction is represented as a list in the format:
        [date (YYYY-MM-DD), category (str), value (str), service (str)].

    transactions2 : list of list
        A list of transactions, where each transaction is represented as a list in the format:
        [date (YYYY-MM-DD), category (str), value (str), service (str)].

    Returns
    -------
    tuple
        - out1 : list of list
            A copy of `transactions1` with an additional field "FOUND" or "MISSING" for each transaction.
        - out2 : list of list
            A copy of `transactions2` with an additional field "FOUND" or "MISSING" for each transaction.

    """
    out1 = [row + ["MISSING"] for row in transactions1]
    out2 = [row + ["MISSING"] for row in transactions2]
    
    not_checked_map = {}
    for i, transaction in enumerate(transactions2):
        date = datetime.strptime(transaction[0], "%Y-%m-%d").date()
        key = (transaction[1], transaction[2], transaction[3])
        if key not in not_checked_map:
            not_checked_map[key] = {}
        if date not in not_checked_map[key]:
            not_checked_map[key][date] = []
        not_checked_map[key][date].append(i)


    for i, transaction in enumerate(out1):
        date = datetime.strptime(transaction[0], "%Y-%m-%d").date()
        valid_dates = {date - timedelta(days=1), date, date + timedelta(days=1)}
        key = (transaction[1], transaction[2], transaction[3])

        if key in not_checked_map:
            min_date = None
            match_index = None

            for valid_date in valid_dates:
                if valid_date in not_checked_map[key]:
                    for idx in not_checked_map[key][valid_date]:
                        if min_date is None or valid_date < min_date:
                            min_date = valid_date
                            match_index = idx

            if match_index is not None:
                out1[i][-1] = "FOUND"
                out2[match_index][-1] = "FOUND"
                not_checked_map[key][min_date].remove(match_index)
                if not not_checked_map[key][min_date]:
                    del not_checked_map[key][min_date]

    return out1, out2