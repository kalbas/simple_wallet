from pydantic import BaseModel, conint


class CreateWalletRequestSchema(BaseModel):
    balance: conint(ge=0) = 0


class RefillRequestSchema(BaseModel):
    amount: conint(ge=0)


class SendMoneyRequestSchema(BaseModel):
    source_wallet_id: int
    target_wallet_id: int
    amount: conint(ge=0)


class WalletResponse(BaseModel):
    id: int
    balance: int

    class Config:
        orm_mode = True
