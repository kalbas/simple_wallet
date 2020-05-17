from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_create_wallet():
    response = client.post(
        '/api/wallet',
        json={'balance': 100}
    )
    assert response.status_code == 201


def test_get_wallet():
    response = client.post(
        '/api/wallet',
        json={'balance': 100}
    )
    assert response.status_code == 201

    wallet_id = response.json().get('id')
    response = client.get(f'/api/wallet/{wallet_id}')
    assert response.status_code == 200
    assert response.json() == {'id': wallet_id, 'balance': 100}


def test_refill_wallet():
    BALANCE = 100
    REFILL_AMOUNT = 40

    response = client.post(
        '/api/wallet',
        json={'balance': BALANCE}
    )
    assert response.status_code == 201

    wallet_id = response.json().get('id')
    response = client.post(
        f'/api/wallet/{wallet_id}/refill',
        json={'amount': REFILL_AMOUNT}
    )
    assert response.status_code == 200
    assert response.json().get('balance') == BALANCE + REFILL_AMOUNT


def test_send_money():
    BALANCE = 200
    AMOUNT = 40

    response = client.post(
        '/api/wallet',
        json={'balance': BALANCE}
    )
    source_wallet_id = response.json().get('id')
    response = client.post(
        '/api/wallet',
        json={'balance': BALANCE}
    )
    target_wallet_id = response.json().get('id')

    response = client.post(
        '/api/transaction',
        json={'source_wallet_id': source_wallet_id, 'target_wallet_id': target_wallet_id, 'amount': AMOUNT}
    )
    assert response.status_code == 201
