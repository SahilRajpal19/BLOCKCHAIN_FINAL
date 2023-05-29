from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,APIRouter
from database import get_db
from blockchain import blockchain
import datetime as dt
import models



router=APIRouter()
blockchain=blockchain()

# endpoint to mine a block
@router.post("/mine_block/", tags=["Blockchain"])
def mine_block(data: str, db: Session = Depends(get_db)):
    if not (db.query(models.BlockchainModel).filter(models.BlockchainModel.id == 1).first()):
        first_block = models.BlockchainModel(id=1, data="Genesisblock", timestamp=str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                             previous_hash="0", proof=1)
        db.add(first_block)
        db.commit()
        db.refresh(first_block)

    block = blockchain.mine_block(data, db)
    print(block, type(block))
    print(block['index'])
    db.add(models.BlockchainModel(id=block["index"], data=block["data"],
           timestamp=block["timestamp"], previous_hash=block["previous_hash"], proof=block["proof"]))

    db.commit()
    return block


# endpoint to return the entire blockchain
@router.get("/blockchain", tags=["Blockchain"])
def get_blockchain(db: Session = Depends(get_db)):
    if not blockchain.is_chain_valid(db):
        return HTTPException(status_code=404, detail="Invalid blockchain")
    # chain = blockchain.chain
    # cur.execute("""SELECT * FROM blocks""")
    # return cur.fetchall()
    return db.query(models.BlockchainModel).all()


# endpoint to see if the chain is valid
@router.get("/validate/", tags=["Blockchain"])
def is_blockchain_valid(db: Session = Depends(get_db)):
    if not blockchain.is_chain_valid(db):
        return HTTPException(status_code=400, detail="The blockchain is invalid")

    return blockchain.is_chain_valid(db)


# endpoint to return the last block
@router.get("/blockchain/last/", tags=["Blockchain"])
def previous_block(db: Session = Depends(get_db)):
    if not blockchain.is_chain_valid(db):
        return HTTPException(status_code=400, detail="The blockchain is invalid")

    return blockchain.get_previous_block(db)


# endpoint to get block hash
@router.get("/hash_by_block_number/{index}", tags=["Blockchain"])
def get_hash_by_block_number(index: int, db: Session = Depends(get_db)):
    # return blockchain.chain[index+1]["previous_hash"]
    # cur.execute(f"""SELECT previous_hash FROM blocks WHERE id={index}""")
    # return cur.fetchone()
    block = db.query(models.BlockchainModel).filter(
        models.BlockchainModel.id == index).first()

    return block.previous_hash


# endpoint to get block by index
@router.get("/block_number/{index}", tags=["Blockchain"])
def get_block_by_index(index: int, db: Session = Depends(get_db)):
    # return blockchain.chain[index-1]
    # cur.execute(f"""SELECT * FROM blocks WHERE id={index}""")
    # return cur.fetchone()

    return db.query(models.BlockchainModel).filter(models.BlockchainModel.id == index).first()


@router.get("/block_between_time/{start_date}/{end_date}", tags=["Blockchain"])
def block_between_time(start_date: str, end_date: str, db: Session = Depends(get_db)):
    if not blockchain.is_chain_valid(db):
        return HTTPException(status_code=404, detail="Invalid blockchain")

    return blockchain.blocks_between_time(start_date, end_date, db)
