from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.services.neo4j_service import add_comment_to_graph

router = APIRouter()

@router.get("/", response_model=List[schemas.Comment])
def read_comments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    bill_id: int = None,
) -> Any:
    """
    Retrieve comments.
    """
    if bill_id:
        comments = crud.crud_comment.get_multi_by_bill(
            db=db, bill_id=bill_id, skip=skip, limit=limit
        )
    else:
        comments = crud.crud_comment.get_multi(db, skip=skip, limit=limit)
    return comments

@router.post("/", response_model=schemas.Comment)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_in: schemas.CommentCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new comment.
    """
    # Verify bill exists
    bill = crud.crud_bill.get(db=db, id=comment_in.bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    comment = crud.crud_comment.create_with_user(
        db=db, obj_in=comment_in, user_id=current_user.id
    )
    # Add to knowledge graph
    add_comment_to_graph(comment)
    return comment

@router.get("/{id}", response_model=schemas.Comment)
def read_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get comment by ID.
    """
    comment = crud.crud_comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/{id}", response_model=schemas.Comment)
def update_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    comment_in: schemas.CommentUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update comment.
    """
    comment = crud.crud_comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = crud.crud_comment.update(db=db, db_obj=comment, obj_in=comment_in)
    return comment

@router.delete("/{id}", response_model=schemas.Comment)
def delete_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete comment.
    """
    comment = crud.crud_comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = crud.crud_comment.remove(db=db, id=id)
    return comment 