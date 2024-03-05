def sum(x, y):
    try:
        if isinstance(x, bool) or isinstance(y, bool):
            return "Error"
        else:
            x = float(x)
            y = float(y)
            res = x+y
            if res.is_integer():
                return int(res)
            else:
                return res
    except ValueError:
        return "Error"
    except TypeError:
        return "Error"