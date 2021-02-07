class ArrayPaginate:
    def __init__(self, array_data, request):
        self.request = request

        paginate_params = self.request.query_params.copy()
        # print(paginate_params)

        self.other_params = ""

        for param in paginate_params:
            if param == "limit" or param == "offset":
                continue

            self.other_params += "&" + param + "=" + paginate_params[param]

        self.limit = int(paginate_params.get('limit', 10))
        self.offset = int(paginate_params.get('offset', 0))

        self.array_data = array_data

        self.count = 0
        self.result_set = dict()

    def fetch(self, **kwargs):

        self.result_set["data"] = self.array_data[self.offset:self.offset + self.limit]
        self.count = len(self.array_data)

        prev_link = None
        next_link = None

        if self.offset - self.limit >= 0:
            prev_link = "offset=" + str(self.offset - self.limit) + "&limit=" + str(self.limit)
            prev_link += "" + self.other_params

        if 0 < len(self.result_set['data']) == self.limit:
            next_link = "offset=" + str(self.offset + self.limit) + "&limit=" + str(self.limit)
            next_link += "" + self.other_params

        host = "https://localhost:9000/"
        if self.request.get_host():
            host = self.request.scheme + "://" + self.request.get_host()

        self.result_set['next'] = host + "?" + next_link if next_link is not None else None
        self.result_set['prev'] = host + "?" + prev_link if prev_link is not None else None
        self.result_set['count'] = self.count

        return self.result_set
