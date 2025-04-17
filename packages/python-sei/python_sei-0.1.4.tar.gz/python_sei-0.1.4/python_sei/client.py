import zeep

from .models import (
    DefinicaoControlePrazo,
    RetornoConsultaProcedimento,  # noqa
    Unidade,
    Usuario,
)
from .sin import encode_sin


class Client:
    def __init__(self, url: str, sigla_sistema: str, identificacao_servico: str):
        self.sigla_sistema = sigla_sistema
        self.identificacao_servico = identificacao_servico
        self.client = zeep.Client(url)

    @property
    def _service(self):
        return self.client.service

    def listar_unidades(
        self,
        id_tipo_procedimento: str = "",
        id_serie: str = "",
    ) -> list[Unidade]:
        """Retorna a lista de unidades cadastradas no SEI"""
        records = self._service.listarUnidades(
            SiglaSistema=self.sigla_sistema,
            IdentificacaoServico=self.identificacao_servico,
            IdTipoProcedimento=id_tipo_procedimento,
            IdSerie=id_serie,
        )
        return Unidade.from_many_records(records)

    def listar_usuarios(
        self,
        id_unidade: str,
        id_usuario: str = "",
    ):
        """Retorna a lista de usuários de uma unidade"""
        records = self._service.listarUsuarios(
            SiglaSistema=self.sigla_sistema,
            IdentificacaoServico=self.identificacao_servico,
            IdUnidade=id_unidade,
            IdUsuario=id_usuario,
        )
        return Usuario.from_many_records(records)

    def consultar_procedimento(
        self,
        id_unidade: str,
        protocolo_procedimento: str,
        retornar_assuntos: bool = False,
        retornar_interessados: bool = False,
        retornar_observacoes: bool = False,
        retornar_andamento_geracao: bool = False,
        retornar_andamento_conclusao: bool = False,
        retornar_ultimo_andamento: bool = False,
        retornar_unidades_procedimento_aberto: bool = False,
        retornar_procedimentos_relacionados: bool = False,
        retornar_procedimentos_anexados: bool = False,
    ):
        record = self._service.consultarProcedimento(
            SiglaSistema=self.sigla_sistema,
            IdentificacaoServico=self.identificacao_servico,
            IdUnidade=id_unidade,
            ProtocoloProcedimento=protocolo_procedimento,
            SinRetornarAssuntos=encode_sin(retornar_assuntos),
            SinRetornarInteressados=encode_sin(retornar_interessados),
            SinRetornarObservacoes=encode_sin(retornar_observacoes),
            SinRetornarAndamentoGeracao=encode_sin(retornar_andamento_geracao),
            SinRetornarAndamentoConclusao=encode_sin(retornar_andamento_conclusao),
            SinRetornarUltimoAndamento=encode_sin(retornar_ultimo_andamento),
            SinRetornarUnidadesProcedimentoAberto=encode_sin(
                retornar_unidades_procedimento_aberto
            ),
            SinRetornarProcedimentosRelacionados=encode_sin(
                retornar_procedimentos_relacionados
            ),
            SinRetornarProcedimentosAnexados=encode_sin(
                retornar_procedimentos_anexados
            ),
        )
        # return record
        return RetornoConsultaProcedimento.from_record(record)

    def definir_controle_prazo(
        self,
        id_unidade: str,
        definicoes: list[DefinicaoControlePrazo],
    ):
        self._service.definirControlePrazo(
            SiglaSistema=self.sigla_sistema,
            IdentificacaoServico=self.identificacao_servico,
            IdUnidade=id_unidade,
            Definicoes=[definicao.to_record() for definicao in definicoes],
        )
