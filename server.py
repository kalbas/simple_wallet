from fastapi import FastAPI, Depends, status, HTTPException, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from config import settings
from models import Wallet, Refill, Transaction, Base
from schemas import CreateWalletRequestSchema, RefillRequestSchema, SendMoneyRequestSchema, WalletResponse


engine = create_engine(settings.database_url)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/api/wallet', response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
def create_wallet(wallet: CreateWalletRequestSchema,
                  db: Session = Depends(get_db)):
    db_wallet = Wallet(balance=wallet.balance)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


@app.get('/api/wallet/{wallet_id}', response_model=WalletResponse)
def get_wallet(wallet_id: int,
               db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if db_wallet:
        return db_wallet
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post('/api/wallet/{wallet_id}/refill', response_model=WalletResponse)
def make_refill(wallet_id: int,
                refill_data: RefillRequestSchema,
                db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not db_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db_wallet.balance += refill_data.amount
    refill_log = Refill(wallet_id=db_wallet.id, amount=refill_data.amount)
    db.add(refill_log)
    db.commit()
    return db_wallet


@app.post('/api/transaction', status_code=status.HTTP_201_CREATED)
def send_money(send_money_command: SendMoneyRequestSchema,
               request: Request,
               db: Session = Depends(get_db)):
    db_source_wallet, db_target_wallet = get_source_and_target_wallets_from_db(send_money_command, db)

    db_source_wallet.balance -= send_money_command.amount
    db_target_wallet.balance += send_money_command.amount

    create_transactions(db, db_source_wallet, db_target_wallet, send_money_command.amount, request.client.host)
    db.commit()


def get_source_and_target_wallets_from_db(data, db):
    db_wallets = db.query(Wallet).filter(
        Wallet.id.in_((data.source_wallet_id, data.target_wallet_id))
    ).with_for_update().all()
    if len(db_wallets) != 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if db_wallets[0].id == data.source_wallet_id:
        return db_wallets[0], db_wallets[1]
    else:
        return db_wallets[1], db_wallets[0]


def create_transactions(db, source_wallet, target_wallet, amount, host):
    source_transaction = Transaction(
        wallet_id=source_wallet.id,
        amount=(-amount),
        ip=host
    )
    db.add(source_transaction)
    target_transaction = Transaction(
        wallet_id=target_wallet.id,
        amount=amount,
        ip=host
    )
    db.add(target_transaction)
