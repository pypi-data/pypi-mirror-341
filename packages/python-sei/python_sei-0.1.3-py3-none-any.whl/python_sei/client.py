import zeep


class Client:
    def __init__(self, url: str, sigla_sistema: str, identificacao_servico: str):
        self.sigla_sistema = sigla_sistema
        self.identificacao_servico = identificacao_servico
        self.client = zeep.Client(url)

    @property
    def _service(self):
        """Retorna o serviço SOAP do SEI"""
        return self.client.service

    def listar_unidades(self, id_tipo_procedimento: str = "", id_serie: str = ""):
        """Lista as unidades cadastradas no SEI"""
        return self._service.listarUnidades(
            SiglaSistema=self.sigla_sistema,
            IdentificacaoServico=self.identificacao_servico,
            IdTipoProcedimento=id_tipo_procedimento,
            IdSerie=id_serie,
        )
