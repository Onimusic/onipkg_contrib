from django.core.exceptions import FieldError
from django.db.models import Q
from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data().replace(u'\xa0', u' ')


def get_default_response_dict() -> dict:
    """Returns the default api response as {data:{items:[], message:str}, status:str}
    """
    return {'data': {'items': [], 'message': 'n/a'}, 'status': get_success_status()}


def get_api_response_dict() -> dict:
    """Returns the default api response as {data:{items:[], message:str}, status:int}
    """
    return {'data': {'items': [], 'message': ''}, 'status': 200}


def get_success_status() -> str:
    """Returns the success status.
    """
    return 'success'


def get_generic_error_status() -> str:
    """Returns the generic error status.
    """
    return 'error'


def get_generic_error_message() -> str:
    """Returns the generic error message.
    """
    return 'Unknown error.'


def get_generic_error404_message() -> str:
    """Returns the generic error message.
    """
    return 'Object not found.'


def get_default_datatables__response(draw=1, records_total=0, records_filtered=0, data=None) -> dict:
    """Returns the generic datatables response.
    """
    if data is None:
        data = []
    return {
        'draw': draw,
        'data': data,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered
    }


def get_default_datatables__cleaned_data(data: list) -> list:
    """ Clean the data to be sent to a datatable
    """

    try:
        response = []
        for item in data:
            cleaned = item
            cleaned['DT_RowId'] = item.get('id')
            response.append(item)
        return response
    except (IndexError, ValueError):
        return data


def default_query_assets_by_args(request, queried_class) -> dict:
    """
        Metodo usado pela api do DataTables para buscar dinamicamente por objetos com base na caixa de busca
        Args:
            request: request da api
            queried_class: classe buscada
        Returns:
            dict contendo a queryset de produtos e outras informacoes relevantes ao DataTables
    """
    request_get_dict = request.GET
    draw = int(
        request_get_dict.get('draw', None))  # parametro padrao do dataTables. n eh necessario nenhuma operacao
    length = int(
        request_get_dict.get('length',
                             None))  # indica quantas linhas vao aparecer na pagina. nao eh necessario operacao
    start = int(
        request_get_dict.get('start', None))  # indica a primeira linha da tabela. nao eh necessario operacao
    search_value = request_get_dict.get('search[value]',
                                        None)  # valor de busca. a queryset deve ser filtrada com base nele
    order_column = int(
        request_get_dict.get('order[0][column]', None))  # indice da coluna que o usuario aplicou ordenacao
    order = request_get_dict.get('order[0][dir]', None)  # indica se eh pra ordenar cresc ou decresc

    order_column = queried_class.get_column_order_choices()[order_column]  # pega qual a coluna eh pra ordenar
    if order == 'desc':
        # se for pra ordenar decrescente, coloca um - na frente (por causa do django orm)
        order_column = '-' + order_column
    if search_value:  # se houver algo na caixa de busca faz o filtro
        queryset = queried_class.filter_objects(searched_value=search_value, request_user=request.user)
    else:
        # se nao houver busca, pega os ultimos mil (o ordering do Meta da classe garante que serao os ultimos)
        try:
            queryset = queried_class.objects.filter(active=True).distinct()
        except FieldError:
            queryset = queried_class.objects.distinct()
        if not request.user.is_staff:
            queryset = queried_class.filter_objects_based_on_user(request_user_profile=request.user.user_user_profile,
                                                                  queryset=queryset)
    # if search_value:  # se houver algo na caixa de busca faz outro filtro alem do de produtos ativos
    #     queryset = queryset.filter(
    #         queried_class.get_filters_for_datatables_api(search_value)
    #     )

    # todo explicar contador tem que contar 2 vezes. com e sem filtro
    count = queryset.count()
    queryset = queryset.order_by(order_column)[
               start:start + length]
    # queryset = queryset[:1000]  # hmmm... sei nao essa linha aqui eim
    return {
        'items': queryset,
        'count': count,
        'draw': draw,
    }


def get_default_datatables__query(request, queryset, search_fields, base_filters=dict()) -> dict:
    """
        Metodo usado pela api do DataTables para buscar dinamicamente por objetos com base na caixa de busca, paginando.
        Args:
            request: request da api
            queryset: queryset padrão do django rest api
            search_fields: campos a serem usados para o like
            base_filters: campos de filtro padrão caso existam
        Returns:
            dict contendo a queryset e outras informacoes relevantes ao DataTables
    """
    count_total = queryset.count()
    request_get_dict = request.GET
    draw = int(
        request_get_dict.get('draw', 0))  # parametro padrao do dataTables. n eh necessario nenhuma operacao
    length = int(
        request_get_dict.get('length',
                             0))  # indica quantas linhas vao aparecer na pagina. nao eh necessario operacao
    start = int(
        request_get_dict.get('start', 0))  # indica a primeira linha da tabela. nao eh necessario operacao
    search_value = request_get_dict.get('search[value]',
                                        None)  # valor de busca. a queryset deve ser filtrada com base nele
    # não fazemos ordenaçõa por enquanto todo
    # order_column = int(
    #     request_get_dict.get('order[0][column]', None))  # indice da coluna que o usuario aplicou ordenacao
    # order = request_get_dict.get('order[0][dir]', None)  # indica se eh pra ordenar cresc ou decresc
    #
    # order_column = queried_class.get_column_order_choices()[order_column]  # pega qual a coluna eh pra ordenar
    # if order == 'desc':
    #     # se for pra ordenar decrescente, coloca um - na frente (por causa do django orm)
    #     order_column = '-' + order_column
    filters = base_filters
    if search_value:  # se houver algo na caixa de busca faz o filtro
        for search_field in search_fields:
            filters[str(search_field) + '__icontains'] = search_value
    #     todo aplicar esse filtro do is staff, agora só testar na verdade
    if not request.user.is_staff:
        queryset = queryset.model.filter_objects_based_on_user(request_user_profile=request.user.user_user_profile,
                                                               queryset=queryset)

    # todo explicar contador tem que contar 2 vezes. com e sem filtro
    count = queryset.count()
    queryset = queryset.filter(**filters).distinct()[start:start + length]
    return {
        'queryset': queryset,
        'count_total': count_total,
        'count': count,
        'draw': draw
    }


def get_url_params(request):
    params = request.query_params
    return f'?{"&".join([str(param) + "=" + str(params[param]) for param in params])}' if params else ''
