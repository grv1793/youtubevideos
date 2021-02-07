class ESPaginate:
    def __init__(self, model, paginate_params, params, sort, size=None, should_send_back_other_params=True):
        paginate_params = paginate_params.copy()

        self.other_params = ""

        for param in paginate_params:
            if param == "limit" or param == "offset":
                continue

            self.other_params += "&" + param + "=" + paginate_params[param]

        self.size = size
        self.limit = int(paginate_params.get('limit', 10))
        self.offset = int(paginate_params.get('offset', 0))

        self.model = model()
        self.filter_params = params
        self.sort_params = sort

        self.count = 0
        self.result_set = None
        self.should_send_back_other_params = should_send_back_other_params

    def fetch(self):
        self.result_set = self.model.query(
            self.limit, self.offset, self.filter_params,
            self.sort_params, size=self.size
        )
        self.count = self.result_set['count']

        prev_link = None
        next_link = None

        if self.offset - self.limit >= 0:
            prev_link = "offset=" + str(self.offset - self.limit) + "&limit=" + str(self.limit)
            if self.should_send_back_other_params:
                prev_link += "" + self.other_params

        if 0 < len(self.result_set['result']) == self.limit:
            next_link = "offset=" + str(self.offset + self.limit) + "&limit=" + str(self.limit)
            if self.should_send_back_other_params:
                next_link += "" + self.other_params

        self.result_set['next'] = next_link
        self.result_set['prev'] = prev_link
        self.result_set['links'] = self.get_paginated_links()

        return self.result_set

    def get_paginated_links(self):
        total_result = self.count

        paginated_links = []

        display_limit = 10

        if (self.offset - (display_limit * self.limit)) >= 0:
            counter = ((self.offset - (display_limit * self.limit)) / self.limit) + 1
            i = (self.offset - (display_limit * self.limit))
        else:
            counter = 1
            i = 0

        is_current = False

        if total_result / self.limit > display_limit * 2:
            loop_limit = display_limit * 2
        else:
            loop_limit = int(total_result / self.limit) + 1

        for loop_counter in range(0, loop_limit):
            if i >= total_result:
                break
            if i == self.offset:
                is_current = True

            params = "offset=" + str(i) + "&limit=" + str(self.limit)
            params += "" + self.other_params
            link = {
                "counter": int(counter),
                "params": params,
                "is_current": is_current
            }

            paginated_links.append(link)
            i += self.limit
            counter += 1
            is_current = False

        return paginated_links
