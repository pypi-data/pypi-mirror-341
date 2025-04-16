class CartesianIterator:
    """
    From a bunch of lists, creates a list by picking elements from each in each
    iteration.

    Example:
        demo = CartesianIterator(["some", "no"],
                                 ["one", "two"],
                                 ["saw it", "took it", "did it"])
        for cartesian in demo:
            print(cartesian)

        # ['some', 'one', 'saw it']
        # ['some', 'one', 'took it']
        # ['some', 'one', 'did it']
        # ['some', 'two', 'saw it']
        # ['some', 'two', 'took it']
        # ['some', 'two', 'did it']
        # ['no', 'one', 'saw it']
        # ['no', 'one', 'took it']
        # ['no', 'one', 'did it']
        # ['no', 'two', 'saw it']
        # ['no', 'two', 'took it']
        # ['no', 'two', 'did it']
    """

    def __init__(self, *cartesian_list: str | list):
        cartesian_list = list(cartesian_list)
        if any([isinstance(item, (list, tuple)) for item in cartesian_list]):
            for index in range(len(cartesian_list)):
                if not isinstance(cartesian_list[index], (list, tuple)):
                    cartesian_list[index] = (cartesian_list[index],)
        else:
            cartesian_list = [cartesian_list]

        self._cartesian_list = cartesian_list
        self._len_cartesian_list = len(self._cartesian_list)
        self._iter_counters = [0] * self._len_cartesian_list
        self._stop_iter_next = False

    def __iter__(self):
        self._iter_counters = [0] * self._len_cartesian_list
        self._stop_iter_next = False
        return self

    def __next__(self):
        if self._stop_iter_next:
            raise StopIteration

        out = []
        for list_num, counter in enumerate(self._iter_counters):
            out.append(self._cartesian_list[list_num][counter])

        self._iter_counters[-1] += 1
        for list_num in range(self._len_cartesian_list - 1, -1, -1):
            if (self._iter_counters[list_num] >=
                    len(self._cartesian_list[list_num])):
                if list_num == 0:
                    self._stop_iter_next = True
                else:
                    self._iter_counters[list_num] = 0
                    self._iter_counters[list_num - 1] += 1

        return out
