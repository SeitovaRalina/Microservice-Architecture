from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.comment import Comment
from src.models.article import Article
from src.models.user import User
from src.schemas import CommentCreate

def add_comment(db: Session, article: Article, current_user: User, comment_in: CommentCreate) -> Comment:
    comment = Comment(body=comment_in.body, author=current_user, article=article)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments(db: Session, article: Article):
    return db.query(Comment).filter(Comment.article_id == article.id).order_by(Comment.created_at.asc()).all()

def delete_comment(db: Session, comment_id: int, current_user: User):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    db.delete(comment)
    db.commit()
    return
