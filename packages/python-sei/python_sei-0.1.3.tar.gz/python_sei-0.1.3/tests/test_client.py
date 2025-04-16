def test_listar_unidades(client):
    unidades = client.listar_unidades()

    print(unidades)
    assert False
