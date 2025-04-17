def test_listar_unidades(client):
    unidades = client.listar_unidades()
    assert len(unidades) >= 0


def test_listar_usuarios(client):
    unidades = client.listar_unidades()
    for unidade in unidades:
        usuarios = client.listar_usuarios(unidade.id_unidade)
        if len(usuarios) == 0:
            continue

        assert usuarios[0].id_usuario != ""
        assert usuarios[0].nome != ""
        assert usuarios[0].sigla != ""
        break
