from python_sei.models import NivelAcesso, Unidade


def test_nivel_acesso_from_str():
    assert NivelAcesso.from_str("0") == NivelAcesso.PUBLICO
    assert NivelAcesso.from_str("1") == NivelAcesso.RESTRITO
    assert NivelAcesso.from_str("2") == NivelAcesso.SIGILOSO


def test_nivel_acesso_to_str():
    assert NivelAcesso.PUBLICO.to_str() == "0"
    assert NivelAcesso.RESTRITO.to_str() == "1"
    assert NivelAcesso.SIGILOSO.to_str() == "2"


def test_unidade():
    records = [
        {
            "IdUnidade": "110001133",
            "Sigla": "SES/URSSJD-NUVISA",
            "Descricao": "Vigilancia Sanitária São João Del Rei",
            "SinProtocolo": "N",
            "SinArquivamento": "S",
            "SinOuvidoria": "S",
        },
        {
            "IdUnidade": "110001135",
            "Sigla": "SES/URSTOF-NUVISA",
            "Descricao": "Vigilancia Sanitária Teófilo Otoni",
            "SinProtocolo": "S",
            "SinArquivamento": "N",
            "SinOuvidoria": "N",
        },
    ]

    unidades = Unidade.from_many_records(records)

    assert len(unidades) == 2

    assert unidades[0].id_unidade == "110001133"
    assert unidades[0].sigla == "SES/URSSJD-NUVISA"
    assert unidades[0].descricao == "Vigilancia Sanitária São João Del Rei"
    assert not unidades[0].protocolo
    assert unidades[0].arquivamento
    assert unidades[0].ouvidoria

    assert unidades[1].id_unidade == "110001135"
    assert unidades[1].sigla == "SES/URSTOF-NUVISA"
    assert unidades[1].descricao == "Vigilancia Sanitária Teófilo Otoni"
    assert unidades[1].protocolo
    assert not unidades[1].arquivamento
    assert not unidades[1].ouvidoria
